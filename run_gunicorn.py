#!/usr/bin/env python
"""Run Flask app with Gunicorn WSGI server - prevents Windows Flask crashes"""
import os
import sys
import socket

# Add project to path
sys.path.insert(0, os.path.dirname(__file__))

# Check if port is available
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('127.0.0.1', 5000))
    s.close()
    print("[OK] Port 5000 is available")
except OSError as e:
    print(f"[ERROR] Port 5000 is in use: {e}")
    sys.exit(1)

from server.app import create_app
from gunicorn.app.base import BaseApplication

class StandaloneApplication(BaseApplication):
    def __init__(self, app, options=None):
        self.application = app
        self.options = options or {}
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

if __name__ == '__main__':
    app = create_app()
    
    options = {
        'bind': '127.0.0.1:5000',
        'workers': 1,
        'threads': 4,
        'worker_class': 'gthread',
        'timeout': 120,
        'accesslog': '-',
        'loglevel': 'info',
        'access_log_format': '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s'
    }
    
    StandaloneApplication(app, options).run()
