#!/usr/bin/env python
"""
Minimal server - no database init, just serve the app
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

# Disable all logging
import logging
for logger_name in ['werkzeug', 'flask', 'urllib3', 'flask.app']:
    logging.getLogger(logger_name).setLevel(logging.CRITICAL)
logging.basicConfig(level=logging.CRITICAL)

print("=" * 70)
print("[*] PC SIMULATOR - STABLE SERVER")
print("=" * 70)
print("[+] Starting on http://127.0.0.1:5000")
print("=" * 70)
print("\n[*] Access URLs:")
print("   [*] Home: http://127.0.0.1:5000/")
print("   [*] Search: http://127.0.0.1:5000/api/search/component")
print("   [*] Health: http://127.0.0.1:5000/health")
print("\n[*] Server is running... Press CTRL+C to stop\n")
print("=" * 70 + "\n")
sys.stdout.flush()

# Import and start app
from server.app import create_app

app = create_app()

# Use the most minimal WSGI server
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    httpd = make_server('127.0.0.1', 5000, app)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
