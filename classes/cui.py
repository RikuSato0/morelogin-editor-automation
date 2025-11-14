#*******************************************************************************
# MPPC UI application
#
# Version 1.00
# Changes:
#   1.00 - Initial version.
#*******************************************************************************
import datetime
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from classes.cbasic import CBasic
from classes.caction import CAction


class CUI(CBasic):
    # Constructor
    def __init__(self, config):
        super().__init__()
        self.logfile = config['Log']['logfile'] if 'Log' in config else 'ui.log'
        self.verbose = False
        self.action  = CAction(config)
        self.version = "1.08"
        # 1.08 - Updated MoreLogin browsers
        # 1.07 - Added MPPC track visit and click API calls, updated MoreLogin browsers
        # 1.06 - Added single screenshots, updated MoreLogin browsers
        # 1.05 - Added multi pages to proxy read in MultiLogin API (new row config.Browser.proxy_pages = 2)


    def EventLoop(self):
        self.CreateMainWindow()
        self.root.mainloop()


    # Create UI for application
    def CreateMainWindow(self):
        title = self.action.GetAppTitle() + " (" + self.version + ")"
        self.root = Tk()
        self.root.title(title)
        self.root.geometry("480x105")
        self.root.attributes('-topmost', True)
        self.root.attributes('-toolwindow', True)
        self.root.protocol("WM_DELETE_WINDOW", self.onClosing)
        width = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight()
        
        #print('DESKTOP', width, height)


        Button(self.root, text="1", width=5, height=2, bg="#a0a0ff", command=self.btnWindow1Click).place(x=10, y=10)
        Button(self.root, text="2", width=5, height=2, bg="#a0a0ff", command=self.btnWindow2Click).place(x=60, y=10)
        Button(self.root, text="3", width=5, height=2, bg="#a0a0ff", command=self.btnWindow3Click).place(x=110, y=10)
        Button(self.root, text="4", width=5, height=2, bg="#a0a0ff", command=self.btnWindow4Click).place(x=10, y=55)
        Button(self.root, text="5", width=5, height=2, bg="#a0a0ff", command=self.btnWindow5Click).place(x=60, y=55)
        Button(self.root, text="6", width=5, height=2, bg="#a0a0ff", command=self.btnWindow6Click).place(x=110, y=55)

        self.photoGrd = PhotoImage(file = r"static/grid.png").subsample(10, 10)
        Button(self.root, text="Grid", width=80, height=80, bg="#a0a0ff", image=self.photoGrd, command=self.btnWindowGridClick).place(x=160, y=10)

        self.photoCam = PhotoImage(file = r"static/camera.png").subsample(20, 20) 
        Button(self.root, text="ScreenShot", width=80, height=80, bg="#ffffa0", image=self.photoCam, command=self.btnScreenShotClick).place(x=270, y=10)

        self.photoRef = PhotoImage(file = r"static/refresh.png").subsample(20, 20) 
        self.btnRefresh = Button(self.root, text="RESTART", width=80, height=80, bg="#a0ffa0", image=self.photoRef, command=self.btnRefreshClick)
        self.btnRefresh.place(x=380, y=10)
        print("f2")

        # Center window
        windowWidth = 480
        windowHeight = 105
        positionRight = int(self.root.winfo_screenwidth()/2 - windowWidth/2)
        positionDown = int(self.root.winfo_screenheight()/2 - windowHeight/2)
        self.root.geometry("+{}+{}".format(positionRight, positionDown))        
        print("f3")


    def onClosing(self):
        self.action.BrowserCloseAll()
        #if messagebox.askokcancel("Quit", "Do you want to quit?"):
        self.root.destroy()


    def btnWindow1Click(self):
        self.action.BrowserSwitch(0)
    def btnWindow2Click(self):
        self.action.BrowserSwitch(1)
    def btnWindow3Click(self):
        self.action.BrowserSwitch(2)
    def btnWindow4Click(self):
        self.action.BrowserSwitch(3)
    def btnWindow5Click(self):
        self.action.BrowserSwitch(4)
    def btnWindow6Click(self):
        self.action.BrowserSwitch(5)

    
    def btnWindowGridClick(self):
        self.action.BrowserSwitchAll()


    def btnScreenShotClick(self):
        idx = self.action.ScreenshotGetMaximizedIndex()
        if idx < 0:
            messagebox.showwarning(title="MPPC Warning", message="Please maximize browser window to make screenshot")
        elif not self.action.ScreenshotCheckSaved(idx):
            self.action.ScreenshotSave(idx, False)
        elif not self.action.ScreenshotCheckSecondSaved():
            if messagebox.askquestion('MPPC Warning', 'Do you want to make second screenshot?') == 'yes':
                self.action.ScreenshotSave(idx, True)
        else:
            messagebox.showwarning(title="MPPC Warning", message="Only one first screenshot per browser and only one second screenshot per session of 6 browsers available.")


    def btnRefreshClick(self):
        self.btnRefresh["state"] = "disabled"
        self.action.BrowserReopenAll()
        self.btnRefresh["state"] = "normal"
