#!/usr/bin/env python
import os, sys
sys.path.insert(0, r'c:\Users\LEENOVO\Desktop\projectk')
import logging
logging.disable(logging.CRITICAL)

try:
    from server.app import create_app
    print('[*] Creating app...')
    app = create_app()
    print('[*] App created successfully')
    
    from wsgiref.simple_server import make_server
    print('[*] Creating server...')
    httpd = make_server('127.0.0.1', 5000, app)
    print('[*] Server created - starting forever...')
    sys.stdout.flush()
    httpd.serve_forever()
except Exception as e:
    print(f'[!] ERROR: {e}')
    import traceback
    traceback.print_exc()
