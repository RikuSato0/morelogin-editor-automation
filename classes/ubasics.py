import configparser, datetime, os, psutil, sys, time


# Check if current script is not executing. Returns False if script execution is in progress
def single_run():
    name = sys.argv[0]
    real = os.path.realpath(sys.argv[0])
    total = 0
    for process in psutil.process_iter():
        if name in process.name() or ('python' in process.name() and (name in process.cmdline()[1] or real in process.cmdline()[1])):
            total += 1
    return total == 1


# Read config values from config file which can be specified as 1st argument
def config_import():
    if (len(sys.argv) > 1):
        config_file = sys.argv[1]
    else:
        config_file = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), 'settings.ini')
    log(f"Config file: {config_file}")
    if (len(sys.argv) > 2):
        custom_file = sys.argv[2]
    else:
        custom_file = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), 'settings-custom.ini')
    config = configparser.ConfigParser()
    if os.path.isfile(custom_file):
        log(f"Config custom file: {custom_file}")
        config.read([config_file, custom_file])
    else:
        config.read(config_file)
    return config


# Logging routine with ability to suppress similar output per second
log_last_msg = ''
log_last_date = datetime.datetime.now()
def log(msg, supress=False, module=None, level=None, fileName=None):
    global log_last_msg, log_last_date
    if not (supress and log_last_msg == msg and (datetime.datetime.now() - log_last_date).total_seconds() < 1):
        log_last_msg = msg
        log_last_date = datetime.datetime.now()
        m = log_last_date.strftime("%Y-%m-%d %H:%M:%S") + '|'
        m += (os.path.basename(sys.argv[0]) if module is None else module) + '|'
        m += ('INFO' if level is None else level) + '|'
        m += msg
        print(m)
        if not fileName is None:
            while True:
                try:
                    if not os.path.isfile(fileName):
                        dirpath = os.path.dirname(fileName)
                        os.makedirs(dirpath, exist_ok=True)
                    with open(fileName, "a") as logfile:
                        logfile.write(m + "\n")
                        return
                except:
                    time.sleep(0.01)
