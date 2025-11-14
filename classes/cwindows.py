#*******************************************************************************
# Windows 32 routines
#
# Version 1.00
# Changes:
#   1.00 - Initial version.
#*******************************************************************************
import pywintypes, sys, win32api, win32con, win32gui
from classes.cbasic import CBasic


class CWindows(CBasic):
    # Constructor
    def __init__(self, config):
        super().__init__()
        #self.redis_command_key = config['Redis']['qrr_command_key']
        self.logfile = config['Log']['logfile'] if 'Log' in config else 'windows.log'
        self.verbose = False


    def GetAllWindowsTitles(self):
        win_list = []
        win32gui.EnumWindows(self.GetAllWindowsTitles_Callback, win_list)
        return win_list


    def GetAllWindowsTitles_Callback(self, hwnd, strings):
        if win32gui.IsWindowVisible(hwnd):
            window_title = win32gui.GetWindowText(hwnd)
            left, top, right, bottom = win32gui.GetWindowRect(hwnd)
            if window_title and right - left and bottom - top:
                strings.append('{}:{}'.format(hwnd, window_title))
        return True


    def ShowWindow(self, handle_int, x, y, w, h):
        try:
            window_handle = pywintypes.HANDLE(handle_int)
            win32gui.ShowWindow(window_handle, win32con.SW_SHOWNORMAL)
            win32gui.MoveWindow(window_handle, x, y, w, h, True)
            win32gui.SetForegroundWindow(window_handle)
            return True
        except:
            return False


    def CloseWindow(self, handle_int):
        try:
            window_handle = pywintypes.HANDLE(handle_int)
            win32gui.PostMessage(window_handle, win32con.WM_CLOSE, 0, 0)
            return True
        except:
            return False


    def MaximizeWindow(self, handle_int):
        try:
            window_handle = pywintypes.HANDLE(handle_int)
            win32gui.ShowWindow(window_handle, win32con.SW_MAXIMIZE)
            win32gui.SetForegroundWindow(window_handle)
            return True
        except:
            return False


    def GetWindowState(self, handle_int):
        try:
            window_handle = pywintypes.HANDLE(handle_int)
            flags, state, ptMin, ptMax, rect = win32gui.GetWindowPlacement(window_handle)
            if state == win32con.SW_MAXIMIZE:
                return 2
            elif state == win32con.SW_MINIMIZE:
                return 0
            return 1
        except:
            return 0

    
    def GetDesktopWidth(self):
        return win32api.GetSystemMetrics(0)


    def GetDesktopHeight(self):
        return win32api.GetSystemMetrics(1)