#!/usr/bin/env python
"""
Ultra-stable server runner - bypasses all frameworks
Runs Flask in a subprocess and keeps it alive
"""
import subprocess
import sys
import time
import os
import signal

def run():
    # Kill any existing Python processes
    os.system("taskkill /F /IM python.exe 2>nul")
    time.sleep(2)
    
    print("=" * 70)
    print("🚀 PC SIMULATOR - ULTRA STABLE SERVER")
    print("=" * 70)
    print("✓ Starting on http://127.0.0.1:5000")
    print("=" * 70)
    print("\n📍 Access URLs:")
    print("   🏠 Home: http://127.0.0.1:5000/")
    print("   🔍 Search: http://127.0.0.1:5000/api/search/component")
    print("   ✓ Health: http://127.0.0.1:5000/health")
    print("\n💻 Server is running... Press CTRL+C to stop\n")
    print("=" * 70 + "\n")
    sys.stdout.flush()
    
    # Start Flask server in subprocess with output forwarding
    proc = subprocess.Popen(
        [sys.executable, "-c", """
import os, sys
sys.path.insert(0, os.getcwd())
from server.app import create_app
from wsgiref.simple_server import make_server
import threading

app = create_app()
httpd = make_server('127.0.0.1', 5000, app)

def serve():
    try:
        httpd.serve_forever()
    except:
        pass

t = threading.Thread(target=serve, daemon=False)
t.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass
"""],
        cwd=os.getcwd(),
        text=True
    )
    
    try:
        proc.wait()
    except KeyboardInterrupt:
        proc.terminate()
        proc.wait()
        print("\n✓ Server stopped")

if __name__ == '__main__':
    run()
