#*******************************************************************************
# MPPC API
#
# Version 1.00
# Changes:
#   1.00 - Initial version.
#*******************************************************************************
import datetime, hashlib, random, requests, uuid
from classes.cbasic import CBasic


class CBrowserMoreLogin(CBasic):
    # Constructor
    def __init__(self, config):
        super().__init__()
        self.base_url = config['Browser']['base_url']
        self.api_id = config['Browser']['api_id']
        self.api_secret = config['Browser']['api_secret']
        self.group_id = int(config['Browser']['group_id'])
        self.timeout = int(config['Browser']['timeout'])
        self.proxy_pages = 2 #int(config['Browser']['proxy_pages'])
        self.logfile = config['Log']['logfile'] if 'Log' in config else 'browser.log'
        self.verbose = False


    ################################################################################
    # PROFILES
    ################################################################################
    def ProfileList(self, filterName = None):
        resp = self._requestPost('api/env/page', {
            "pageNo" : "1",
            "pageSize" : "100"
        })
        results = []
        if resp.ok:
            resp = resp.json()
            for env in resp['data']['dataList']:
                if filterName is None or filterName in env['envName']:
                    results.append({
                        'id': env['id'],
                        'name': env['envName']
                    })
        return results


    def ProfileCreateRandom(self, name, proxyId, openUrl):
        configs = [ # OS(1-Win, 2-Mac)-Browser(1-Chrome, 2-FF)-Version
            '1-1-133',
            '1-1-132',
            '1-1-132',
            '1-1-131',
            '1-1-131',
            '1-1-130',
            '1-2-132',
            '1-2-132',
            '1-2-129',
            '2-1-133',
            '2-1-132',
            '2-1-131',
        ]
        config = random.choice(configs)
        print('Profile config:', config)
        [operatorSystemId, browserTypeId, kernelVersion] = config.split('-')
        #browserTypeId    = 1 if random.randint(0, 100) <= 70 else 2
        #operatorSystemId = 1 if random.randint(0, 100) <= 90 else 2
        return self.ProfileCreate(name, proxyId, int(operatorSystemId), int(browserTypeId), int(kernelVersion), openUrl)


    def ProfileCreate(self, name, proxyId, operatorSystemId, browserTypeId, kernelVersion, openUrl):
        resp = self._requestPost('api/env/create/advanced', {
        	"advancedSetting": {},
        	"afterStartupConfig": {
        		"afterStartup": 2,
        		"autoOpenUrls": [openUrl]
        	},
        	"browserTypeId": browserTypeId, # 1-Chrome, 2-Firefox
        	"envName": name,
        	"groupId": self.group_id,
        	"operatorSystemId": operatorSystemId, # 1-Windows, 2-macOS
        	"proxyId": proxyId,
       	    "uaVersion": kernelVersion,
        })
        if resp.ok:
            data = resp.json()
            #print(data)
            if int(data['code']) == 0:
                return int(data['data'])
        return None


    def ProfileStart(self, envId):
        resp = self._requestPost('api/env/start', {
            'envId' : str(envId)
        })
        if resp.ok:
            data = resp.json()
            if int(data['code']) == 0:
                return True
        return False


    def ProfileClose(self, envId):
        resp = self._requestPost('api/env/close', {
            'envId' : str(envId)
        })
        if resp.ok:
            data = resp.json()
            if int(data['code']) == 0:
                return True
        return False

    
    def ProfileCloseAll(self, filterName = None):
        results = self.ProfileList(filterName);
        for env in results:
            resp = self.ProfileClose(env['id'])


    def ProfileDelete(self, ids):
        resp = self._requestPost('api/env/removeToRecycleBin/batch', {
            'envIds' : ids
        })
        return resp

    
    def ProfileDeleteAll(self, filterName = None):
        results = self.ProfileList(filterName);
        ids = []
        for p in results:
            ids.append(p['id'])
        if len(ids) > 0:
            resp = self.ProfileDelete(ids)
            return resp.ok
        return True



    ################################################################################
    # PROXIES
    ################################################################################
    def ProxyList(self, filterName = None):
        page = 1
        results = []
        while page <= self.proxy_pages:
            resultsPage = self.ProxyListPage(page, filterName)
            if len(resultsPage) > 0:
                results.extend(resultsPage)
            page += 1
        return results


    def ProxyListPage(self, page, filterName = None):
        resp = self._requestPost('api/proxyInfo/page', {
            "pageNo" : str(page),
            "pageSize" : "100"
        })
        results = []
        if resp.ok:
            resp = resp.json()
            for env in resp['data']['dataList']:
                if filterName is None or filterName in env['proxyName']:
                    results.append({
                        'id': int(env['id']),
                        'name': env['proxyName']
                    })
        return results

    
    def ProxyCreate(self, name, ip, port, username, password):
        resp = self._requestPost('api/proxyInfo/add', {
            'proxyName': name,
            'proxyIp': ip,
            'proxyPort': port,
            'username': username,
            'password': password,
            'proxyProvider': 2, # socks5
        })
        return resp

    
    def ProxyUpdate(self, proxyId, name, ip, port, username, password):
        resp = self._requestPost('api/proxyInfo/update', {
            'id': proxyId,
            'proxyName': name,
            'proxyIp': ip,
            'proxyPort': port,
            'username': username,
            'password': password,
            'proxyProvider': 2, # socks5
        })
        return resp

    
    def ProxyDelete(self, ids):
        resp = self._requestPost('api/proxyInfo/delete', {
            'ids' : ids
        })
        return resp

    
    def ProxyDeleteAll(self):
        results = self.ProxyList();
        ids = []
        for p in results:
            ids.append(p['id'])
        if len(ids) > 0:
            resp = self.ProxyDelete(ids)
            return resp.ok
        return True

    
    def ProxyCreateDefault(self, total, namePref):
        results = self.ProxyList(namePref)
        if len(results) < total:
            for i in range(total - len(results)):
                resp = self.ProxyCreate(namePref + str(i), '1.1.1.1', 1, 'u1', 'p1')
        results = self.ProxyList(namePref)
        return results
        

    ################################################################################
    # COMMON
    ################################################################################
    def _requestPost(self, path, params):
        timestamp = round((datetime.datetime.now(tz=datetime.timezone.utc) - datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)).total_seconds())
        nonceId = str(timestamp) + ":" + str(uuid.uuid4())
        auth = hashlib.md5((self.api_id + nonceId + self.api_secret).encode()).hexdigest()
        headers = {
            "Content-Type" : "application/json",
            "X-Api-Id" : self.api_id,
            "X-Nonce-Id" : nonceId,
            "Authorization" : auth
        }
        resp = requests.post(self.base_url + path, json=params, headers=headers, timeout=self.timeout)
        print('----------', path)
        print(resp.json())
        print('----------')
        return resp
