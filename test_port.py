#!/usr/bin/env python
"""Test server on different port"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

import logging
logging.getLogger('werkzeug').setLevel(logging.ERROR)
logging.getLogger('flask').setLevel(logging.ERROR)

from server.app import create_app

app = create_app()
print("Starting on port 8080...")
sys.stdout.flush()

app.run(
    host='127.0.0.1',
    port=8080,
    debug=False,
    use_reloader=False,
    use_debugger=False,
    threaded=True,
)
