#!/usr/bin/python3
import json, sys, traceback
from classes.ubasics import *
from classes.cui import CUI


# Main function
def main():
    log("*** Starting MPPC UI application ***")
    #if (not single_run()):
    #    log("ERROR! Another instance already running")
    #    return
    config = config_import()
    logfile = config['Log']['logfile']
    log("Started MPPC UI application", module='MppcUI', level='INFO', fileName=logfile)
    try:
        ui = CUI(config)
        ui.EventLoop()
    except:
        traceback.print_exception(*sys.exc_info())
        log(json.dumps(traceback.format_exception(*sys.exc_info())), module='MppcUI', level='ERROR', fileName=logfile)


# Start main routine
if __name__ == "__main__":
    main()
