#!/usr/bin/python3
#*******************************************************************************
# Implements basic functionality for all the classes.
#
# Version 1.00
# Changes:
#   1.00 - Initial version.
#*******************************************************************************
import configparser, datetime, os, sys, time

class CBasic:
    # Constructor
    def __init__(self):
        if (len(sys.argv) > 2):
            custom_file = sys.argv[2]
        else:
            custom_file = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), 'settings-custom.ini')
        if os.path.isfile(custom_file):
            self.config_custom_file = custom_file
        else:
            self.config_custom_file = None


    # Get custom config value from file if exists
    def getCustomConfigValue(self, section, key):
        if self.config_custom_file is None:
            raise Exception('Custom config file not found')
        else:
            config = configparser.ConfigParser()
            config.read(self.config_custom_file)
            return config[section][key]


    # Update custom config file if exists
    def setCustomConfigValue(self, section, key, value):
        if self.config_custom_file is None:
            raise Exception('Custom config file not found')
        else:
            config = configparser.ConfigParser()
            config.read(self.config_custom_file)
            config[section][key] = value
            with open(self.config_custom_file, 'w') as f:
                config.write(f)


    # Logging routine with ability to suppress similar output per second
    log_last_msg = ''
    log_last_msg_count = 0
    log_last_date = datetime.datetime.now()
    logfile = None
    logmodule = None
    def log(self, msg, supress=False, suppress_interval_sec=1, module=None, level=None, fileName=None):
        if not (supress and self.log_last_msg == msg and (datetime.datetime.now() - self.log_last_date).total_seconds() < suppress_interval_sec):
            self.log_last_date = datetime.datetime.now()
            count_suffix = ''
            if self.log_last_msg_count > 1:
                count_suffix = f" (x{self.log_last_msg_count})"
            m = self.log_last_date.strftime("%Y-%m-%d %H:%M:%S") + '|'
            module = self.logmodule if module is None else module
            m += (os.path.basename(sys.argv[0]) if module is None else module) + '|'
            m += ('INFO' if level is None else level) + '|'
            m += msg + count_suffix
            print(m)
            fileName = self.logfile if fileName is None else fileName
            if not fileName is None:
                while True:
                    try:
                        with open(fileName, "a") as logfile:
                            logfile.write(m + "\n")
                            return
                    except:
                        time.sleep(0.01)
            self.log_last_msg = msg
            self.log_last_msg_count = 1
        else:
            self.log_last_msg_count += 1
