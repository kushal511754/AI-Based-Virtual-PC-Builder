#!/usr/bin/env python
"""
Simple HTTP wrapper for the Flask app using werkzeug directly
Avoids Flask's development server issues
"""
import os
import sys
from threading import Thread

sys.path.insert(0, os.path.dirname(__file__))

from server.app import create_app
from werkzeug.serving import make_server

app = create_app()

print("=" * 60)
print("STARTING PC SIMULATOR SERVER (WSGI)")
print("=" * 60)
print("Server initialized on http://127.0.0.1:5000")
print("Press Ctrl+C to stop")
print("=" * 60)

# Create WSGI server directly (more stable than app.run())
server = make_server('127.0.0.1', 5000, app, threaded=True)

try:
    server.serve_forever()
except KeyboardInterrupt:
    print("\nServer stopped")
    sys.exit(0)
