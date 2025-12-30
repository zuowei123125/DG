import psutil

def is_coreldraw_running():
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'] == "CorelDRW.exe":
            return True
    return False