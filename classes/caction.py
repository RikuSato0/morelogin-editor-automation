#*******************************************************************************
# Business logic actions
#
# Version 1.00
# Changes:
#   1.00 - Initial version.
#*******************************************************************************
import datetime, pywintypes, threading, time
from PIL import ImageGrab
from classes.cbasic import CBasic
from classes.cbrowsermorelogin import CBrowserMoreLogin
from classes.cmppcapi import CMppcApi
from classes.cwindows import CWindows


class CAction(CBasic):
    # Constructor
    def __init__(self, config):
        super().__init__()
        #self.redis_command_key = config['Redis']['qrr_command_key']
        self.browser_title = config['Process']['browser_title']
        self.screenshot_path = config['Process']['screenshot_path']
        self.traflist = config['MppcApi']['traflist']
        self.logfile = config['Log']['logfile'] if 'Log' in config else 'action.log'
        self.verbose = False
        self.total   = 6
        self.mppc = CMppcApi(config)
        self.bro = CBrowserMoreLogin(config)
        self.win = CWindows(config)
        self.desk_width = self.win.GetDesktopWidth()
        self.desk_height = self.win.GetDesktopHeight()
        self.threads = []
        self.brolist = [None] * self.total
        self.trafdata = [None] * self.total
        self.proxies = []
        self.screenshots = [None] * self.total
        self.screenSecond = False


    def GetAppTitle(self):
        self.mppc.Login()
        results = self.mppc.AgentTrafListSearch(self.traflist)
        print(results)
        if len(results['traflists']) > 0:
            #for row in results['traflists']:
            return results['traflists'][0]['name']
        else:
            return 'MPPC'
        

    def BrowserReopenAll_Prepare(self):
        tlist = []
        
        # Start thread to close and cleanup profiles and to create default proxies
        t = threading.Thread(target=self.threadBrowserCleanup)
        t.start()
        tlist.append(t)

        # MPPC login
        start = time.time()
        self.mppc.Login()
        #print('MPPC Login', (time.time() - start))

        # MPPC traf lists
        self.trafdata = [None] * self.total
        for i in range(self.total):
            t = threading.Thread(target=self.threadMppcTrafList, args=[i])
            t.start()
            tlist.append(t)

        # Wait till all threads end
        is_alive = True
        while is_alive:
            is_alive = False
            for t in tlist:
                is_alive = is_alive or t.is_alive()
            time.sleep(0.1)
        
        # Check number of existing proxies
        if len(self.proxies) != self.total:
            raise Exception('Error creating default proxies')
        #print('===== PREPARE END')


    def threadBrowserCleanup(self):
        self.proxies = []
        start = time.time()
        self.BrowserCloseAll()
        #print('BrowserCloseAll', (time.time() - start))
        start = time.time()
        self.bro.ProfileCloseAll(self.browser_title)
        #print('ProfileCloseAll', (time.time() - start))
        start = time.time()
        self.bro.ProfileDeleteAll(self.browser_title)
        #print('ProfileDeleteAll', (time.time() - start))
        start = time.time()
        self.proxies = self.bro.ProxyCreateDefault(self.total, self.browser_title)
        #print('ProxyCreateDefault', (time.time() - start))


    def threadMppcTrafList(self, idx):
        start = time.time()
        print(f'MPPC Thread start {idx}')
        time.sleep(float(idx) / 2 + 0.1)
        try:
            traf = self.mppc.AgentTrafList()
            print(f'MPPC Thread {idx} - API Response: {traf}')
            self.trafdata[idx] = traf
        except Exception as e:
            print(f'MPPC Thread {idx} - ERROR calling AgentTrafList: {e}')
            self.trafdata[idx] = None
        print(f'MPPC Thread end {idx}, time: {time.time() - start}')


    def BrowserReopenAll(self):
        self.BrowserReopenAll_Prepare()
     
        # Create threads to open browser window
        start = time.time()
        tlist = []
        for i in range(self.total):
            t = threading.Thread(target=self.threadReopenBrowser, args=[i, self.proxies[i]['id']])
            t.start()
            tlist.append(t)
        print('Create threads', (time.time() - start))

        # Wait till all the threads completion
        print("Waiting")
        self.brolist = [None] * self.total
        self.screenshots = [None] * self.total
        self.screenSecond = False
        wlist = []
        is_alive = True
        started = 0
        while is_alive and started < self.total:
            is_alive = False
            for t in tlist:
                is_alive = is_alive or t.is_alive()
            wnds = self.win.GetAllWindowsTitles()
            for w in wnds:
                if self.browser_title in w:
                    if not w in wlist:
                        wlist.append(w)
                        row = w.split(':')
                        idx = int(row[1][-1:])
                        self.brolist[idx] = int(row[0])
                        self.BrowserPlace(idx)
                        started += 1
            time.sleep(0.2)
        
        # Relocate all windows
        for w in wlist:
            self.brolist[idx] = int(row[0])
            self.BrowserPlace(idx)


    def threadReopenBrowser(self, idx, proxyId):
        start = time.time()
        print('Thread start', idx)
        traf = self.trafdata[idx]
        
        # Debug: Print the traffic data structure
        print(f'Thread {idx} - Traffic data: {traf}')
        
        # Check if traf is None or doesn't have expected structure
        if traf is None:
            print(f'Thread {idx} - ERROR: Traffic data is None')
            return
            
        if 'sites' not in traf:
            print(f'Thread {idx} - ERROR: No "sites" key in traffic data')
            print(f'Thread {idx} - Available keys: {list(traf.keys()) if isinstance(traf, dict) else "Not a dict"}')
            return
            
        if not traf['sites'] or len(traf['sites']) == 0:
            print(f'Thread {idx} - WARNING: Sites array is empty, using default values')
            # Use default values when no sites are available
            proxy = {
                'ip': '127.0.0.1',
                'port': '1080',
                'login': 'default',
                'pass': 'default'
            }
            url = 'https://www.google.com'
        else:
            start = time.time()
            try:
                proxy = traf['sites'][0]['proxy']
                url   = traf['sites'][0]['url']
            except (KeyError, IndexError) as e:
                print(f'Thread {idx} - ERROR: Failed to access proxy/url data: {e}')
                print(f'Thread {idx} - Sites[0] structure: {traf["sites"][0] if traf["sites"] else "Empty"}')
                return
            
        self.bro.ProxyUpdate(proxyId, self.browser_title + str(idx), proxy['ip'], proxy['port'], proxy['login'], proxy['pass'])
        #print('ProxyUpdate', idx, (time.time() - start))
        start = time.time()
        profileId = self.bro.ProfileCreateRandom(self.browser_title + str(idx), proxyId, url)
        #print('ProfileCreateRandom', idx, (time.time() - start))
        start = time.time()
        if not profileId is None:
            self.bro.ProfileStart(profileId)
            #print('ProfileStart', idx, (time.time() - start))
        print('========== Thread end', idx, )


    def BrowserCloseAll(self):
        for b in self.brolist:
            if not b is None:
                self.win.CloseWindow(b)


    # Maximize/normilize required window and normalize others
    def BrowserSwitch(self, idx):
        isMax = False
        b = self.brolist[idx]
        if not b is None:
            isMax = self.win.GetWindowState(b) == 2
        self.BrowserSwitchAll()
        if not b is None and not isMax:
            self.win.MaximizeWindow(b)

    
    def BrowserSwitchAll(self):
        for idx in range(self.total):
            b = self.brolist[idx]
            if not b is None:
                self.BrowserPlace(idx)


    def BrowserPlace(self, idx):
        b = self.brolist[idx]
        if not b is None:
            wrows = 2
            wcols = int(self.total / wrows)
            ww = int(self.desk_width / wcols)
            wh = int(self.desk_height / wrows)
            x = (idx % wcols) * ww
            y = int(idx / wcols) * wh
            #print('POSITIONS', wcols, wrows, idx, x, y, ww, wh)
            self.win.ShowWindow(b, x, y, ww, wh)


    ################################################################################
    # Screenshots
    ################################################################################

    
    def ScreenshotGetMaximizedIndex(self):
        for i in range(self.total):
            b = self.brolist[i]
            if not b is None:
                st = self.win.GetWindowState(b)
                if st == 2:
                    return i
        return -1


    def ScreenshotCheckSaved(self, idx):
        return not self.screenshots[idx] is None

    
    def ScreenshotCheckSecondSaved(self):
        return self.screenSecond


    def ScreenshotSave(self, idx, isSecond):
        b = self.brolist[idx]
        secondSuffix = '-second' if isSecond else ''
        img = ImageGrab.grab()
        img.save(self.screenshot_path + 'screenshot-' + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + secondSuffix + '.jpg')
        self.screenshots[idx] = True
        if isSecond:
            self.screenSecond = True
        self.MppcRecordVisit(idx, isSecond)

    
    def MppcRecordVisit(self, idx, isSecond):
        traf     = self.trafdata[idx]
        if isSecond:
            level_id = traf['sites'][0]['levels'][0]['id']
            self.mppc.StatisticsClickSave(level_id)
        else:
            site_id  = traf['sites'][0]['id']
            proxy_id = traf['sites'][0]['proxy']['id']
            self.mppc.StatisticsVisitSave(site_id, proxy_id)


    def OLD_ScreenshotSave(self):
        is_brow = False
        for b in self.brolist:
            if not b is None:
                st = self.win.GetWindowState(b)
                if st == 2:
                    is_brow = True
        if is_brow:
            img = ImageGrab.grab()
            img.save(self.screenshot_path + 'screenshot-' + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '.jpg')
        return is_brow
            