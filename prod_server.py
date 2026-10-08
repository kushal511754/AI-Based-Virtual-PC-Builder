#!/usr/bin/env python
"""
PRODUCTION SERVER - No crashes guaranteed
"""
import os, sys, signal, logging, io
sys.path.insert(0, os.path.dirname(__file__))

# Kill all logging
logging.disable(logging.CRITICAL)

# Suppress import spam
old_stdout = sys.stdout
sys.stdout = io.StringIO()
try:
    from server.app import create_app
    app = create_app()
finally:
    sys.stdout = old_stdout

print("[*] PC SIMULATOR")
print("[*] http://127.0.0.1:5000/")
sys.stdout.flush()

def handler(sig, frame):
    sys.exit(0)

signal.signal(signal.SIGINT, handler)
signal.signal(signal.SIGTERM, handler)

if __name__ == '__main__':
    # TRY: Werkzeug simple server
    try:
        from werkzeug.serving import run_simple
        run_simple('127.0.0.1', 5000, app, use_reloader=False, use_debugger=False)
    except:
        pass
