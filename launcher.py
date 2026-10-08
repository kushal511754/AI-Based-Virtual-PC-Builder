#!/usr/bin/env python
"""
Master server launcher - keeps wsgiref alive in subprocess
"""
import subprocess
import sys
import time
import os
import signal

os.system("taskkill /F /IM python.exe 2>nul")
time.sleep(2)

code = """
import os, sys
sys.path.insert(0, r'c:\\Users\\LEENOVO\\Desktop\\projectk')
import logging
logging.disable(logging.CRITICAL)

from server.app import create_app
from wsgiref.simple_server import make_server

app = create_app()
httpd = make_server('127.0.0.1', 5000, app)
print('[*] SERVER RUNNING')
sys.stdout.flush()
try:
    httpd.serve_forever()
except:
    pass
"""

print("[*] PC SIMULATOR - Starting Server on http://127.0.0.1:5000")
print("[*] Access: http://127.0.0.1:5000/")
print("[*] Search: http://127.0.0.1:5000/api/search/component")
print()

proc = subprocess.Popen([sys.executable, '-c', code])
try:
    proc.wait()
except KeyboardInterrupt:
    proc.terminate()
