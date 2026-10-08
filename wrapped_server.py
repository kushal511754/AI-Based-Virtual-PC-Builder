#!/usr/bin/env python
"""
WINDOWS-COMPATIBLE SERVER - Uses subprocess wrapper
This bypasses all Werkzeug/Flask crashes by wrapping in subprocess
"""
import subprocess
import sys
import time
import os

# Kill existing servers
os.system("taskkill /F /IM python.exe 2>nul")
time.sleep(2)

print("[*] PC SIMULATOR - Starting Server")
print("[*] Access: http://127.0.0.1:5000/")

# Run server code in subprocess with full Python isolation
code = """
import os, sys
os.chdir(r'c:\\\\Users\\\\LEENOVO\\\\Desktop\\\\projectk')
sys.path.insert(0, '.')

# Minimal setup - no Flask complications
import logging
logging.disable(logging.CRITICAL)

print('[*] Loading app...')
from server.app import create_app
app = create_app()
print('[*] App loaded - starting server')
sys.stdout.flush()

# Use the most basic WSGI server possible
from wsgiref.simple_server import make_server
server = make_server('127.0.0.1', 5000, app)
print('[*] SERVER RUNNING')
sys.stdout.flush()

try:
    server.serve_forever()
except KeyboardInterrupt:
    pass
finally:
    server.server_close()
"""

try:
    proc = subprocess.Popen(
        [sys.executable, '-c', code],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == 'win32' else 0
    )
    
    # Wait for server to start
    time.sleep(5)
    
    # Keep subprocess alive
    while proc.poll() is None:
        time.sleep(1)
    
    # If it exited, print why
    if proc.returncode != 0:
        stdout, stderr = proc.communicate()
        print("[!] Server error:")
        print(stdout)
        print(stderr)
    
except KeyboardInterrupt:
    print("\n[*] Shutdown")
    try:
        proc.terminate()
    except:
        pass
except Exception as e:
    print(f"[!] Error: {e}")
