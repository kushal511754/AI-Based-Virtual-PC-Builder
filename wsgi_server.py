#!/usr/bin/env python
"""Gunicorn production server - bulletproof"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

if __name__ == '__main__':
    from server.app import create_app
    app = create_app()
    
    # Run with gunicorn
    import gunicorn.app.base
    
    class StandaloneApplication(gunicorn.app.base.BaseApplication):
        def __init__(self, app, options=None):
            self.application = app
            self.options = options or {}
            super().__init__()

        def load_config(self):
            for key, value in self.options.items():
                self.cfg.set(key.lower(), value)

        def load(self):
            return self.application

    options = {
        'bind': '127.0.0.1:5000',
        'workers': 1,
        'threads': 4,
        'timeout': 120,
        'keepalive': 5,
        'access_log_format': '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s',
    }
    
    StandaloneApplication(app, options).run()
