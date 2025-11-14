#*******************************************************************************
# MPPC API
#
# Version 1.00
# Changes:
#   1.00 - Initial version.
#*******************************************************************************
import requests
from classes.cbasic import CBasic


class CMppcApi(CBasic):
    # Constructor
    def __init__(self, config):
        super().__init__()
        self.base_url = config['MppcApi']['base_url']
        self.login = config['MppcApi']['login']
        self.password = config['MppcApi']['password']
        self.traflist = config['MppcApi']['traflist']
        self.logfile = config['Log']['logfile'] if 'Log' in config else 'action.log'
        self.verbose = False


    def Login(self):
        self.session = requests.Session()
        try:
            response = self.session.post(self.base_url + 'admin/login/', data={
                'api': '1',
                'AdminLoginForm[email]': self.login,
                'AdminLoginForm[password]': self.password,
                'AdminLoginForm[rememberMe]': '1',
            })
            print(f'MPPC Login Response Status: {response.status_code}')
            print(f'MPPC Login Response: {response.text[:200]}...')  # First 200 chars
        except Exception as e:
            print(f'MPPC Login ERROR: {e}')
            raise


    def AgentTrafList(self):
        try:
            url = self.base_url + 'admin/agent/sitetraflist?uid=' + self.traflist
            print(f'MPPC AgentTrafList URL: {url}')
            response = self.session.get(url)
            print(f'MPPC AgentTrafList Status: {response.status_code}')
            print(f'MPPC AgentTrafList Response: {response.text[:500]}...')  # First 500 chars
            return response.json()
        except Exception as e:
            print(f'MPPC AgentTrafList ERROR: {e}')
            raise


    def AgentTrafListSearch(self, uid = ''):
        response = self.session.get(self.base_url + 'admin/agent/sitetraflistsearch?uid=' + uid)
        return response.json()


    def StatisticsVisitSave(self, site_id, proxy_id):
        response = self.session.post(self.base_url + 'admin/statistics/trackvisit', data={
            'siteId': site_id,
            'proxyId': proxy_id,
            'proxyIp': '',
        })
        print("MPPC Track Visit:")
        print(response)


    def StatisticsClickSave(self, level_id):
        response = self.session.post(self.base_url + 'admin/statistics/trackclick', data={
            'levelId': level_id,
        })
        print("MPPC Track Click:")
        print(response)
