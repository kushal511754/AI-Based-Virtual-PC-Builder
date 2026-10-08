#!/usr/bin/env python
"""Direct server runner - bypasses Flask app.run() issues"""
import os
import sys
import logging

sys.path.insert(0, os.path.dirname(__file__))

# Minimal logging
logging.basicConfig(level=logging.CRITICAL)
for logger_name in ['werkzeug', 'flask']:
    logging.getLogger(logger_name).setLevel(logging.CRITICAL)

print("=" * 70)
print("🚀 STARTING PC SIMULATOR SERVER")
print("=" * 70)

try:
    from server.app import create_app
    from werkzeug.serving import run_simple
    
    app = create_app()
    
    print("✓ App initialized")
    print("✓ Server: http://127.0.0.1:5000")
    print("✓ Press CTRL+C to stop")
    print("=" * 70)
    
    # Use Werkzeug directly to avoid Flask app.run() issues
    run_simple(
        '127.0.0.1',
        5000,
        app,
        use_reloader=False,
        use_debugger=False,
        threaded=True
    )
except KeyboardInterrupt:
    print("\n✓ Server stopped")
    sys.exit(0)
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
