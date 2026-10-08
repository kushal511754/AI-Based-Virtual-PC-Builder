#!/usr/bin/env python
"""
Debug server - trace all errors
"""
import os
import sys
import traceback

sys.path.insert(0, os.path.dirname(__file__))

# Disable logging to avoid encoding issues
import logging
for logger_name in ['werkzeug', 'flask', 'urllib3']:
    logging.getLogger(logger_name).setLevel(logging.CRITICAL)
logging.basicConfig(level=logging.CRITICAL)

try:
    print("[*] PC SIMULATOR - STABLE SERVER")
    print("[+] Starting on http://127.0.0.1:5000")
    print("[*] Access URLs:")
    print("   [*] Home: http://127.0.0.1:5000/")
    print("   [*] Search: http://127.0.0.1:5000/api/search/component")
    print("[*] Server is running... Press CTRL+C to stop\n")
    sys.stdout.flush()
    
    print("[*] Importing Flask app...")
    sys.stdout.flush()
    
    from server.app import create_app
    print("[+] App imported successfully")
    sys.stdout.flush()
    
    print("[*] Creating Flask app...")
    sys.stdout.flush()
    
    app = create_app()
    print("[+] Flask app created successfully")
    sys.stdout.flush()
    
    print("[*] Creating WSGI server...")
    sys.stdout.flush()
    
    from wsgiref.simple_server import make_server
    httpd = make_server('127.0.0.1', 5000, app)
    print("[+] WSGI server created successfully")
    sys.stdout.flush()
    
    print("[*] Starting serve_forever()...")
    sys.stdout.flush()
    
    httpd.serve_forever()
    
except KeyboardInterrupt:
    print("\n[*] Server stopped")
    try:
        httpd.server_close()
    except:
        pass
except Exception as e:
    print(f"\n[!] ERROR: {type(e).__name__}: {e}")
    traceback.print_exc()
    sys.exit(1)
