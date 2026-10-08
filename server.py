#!/usr/bin/env python
import os, sys, time
sys.path.insert(0, os.path.dirname(__file__))

# Disable logging
import logging
logging.disable(logging.CRITICAL)

from server.app import create_app
from wsgiref.simple_server import make_server

app = create_app()
httpd = make_server('127.0.0.1', 5000, app)

print("[*] PC SIMULATOR Server on http://127.0.0.1:5000")
print("[*] Press CTRL+C to stop")
sys.stdout.flush()

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass
finally:
    httpd.server_close()
