import os
import sys
import time
import webview
from threading import Thread
import signal
import subprocess
# import webbrowser

def kill_port_8000():
    command = "netstat -ano | findstr 8000"
    c = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr = subprocess.PIPE)
    stdout, stderr = c.communicate()
    pid = int(stdout.decode().strip().split(' ')[-1])
    os.kill(pid, signal.SIGTERM)
    
def start_webview():
    window = webview.create_window('A-Eye Diagnostics', 'http://localhost:8000/', confirm_close=True, fullscreen=False, width=1440, height=900)
    webview.start()
    window.closed = os._exit(0)
    kill_port_8000()

def start_startdjango():
    if sys.platform in ['win32', 'win64']:
        os.system(".\\.venv\\Scripts\\python.exe manage.py runserver {}:{}".format('0.0.0.0', '8000'))
    else:
        os.system(".\\.venv\\Scripts\\python3.exe manage.py runserver {}:{}".format('127.0.0.1', '8000'))

if __name__ == '__main__':
    Thread(target=start_startdjango).start()
    time.sleep(3)
    start_webview()
    # webbrowser.open_new('http://localhost:8000/')
