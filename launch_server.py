#!/usr/bin/env python
"""Stable server with threading fallback"""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))

# Suppress verbose logging
import logging
logging.getLogger('werkzeug').setLevel(logging.ERROR)
logging.getLogger('flask').setLevel(logging.ERROR)

print("=" * 70)
print("🚀 PC SIMULATOR - STARTING SERVER")
print("=" * 70)

try:
    from server.app import create_app
    
    app = create_app()
    print("✓ Application created successfully")
    
    # Try different server approaches
    print("✓ Attempting to start server...")
    print("=" * 70)
    
    # Set up server to run indefinitely
    sys.stdout.flush()
    sys.stderr.flush()
    
    # Use Flask's built-in run with explicit settings
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=False,
        use_reloader=False,
        use_debugger=False,
        threaded=True,
    )
    
except KeyboardInterrupt:
    print("\n✓ Server stopped")
    sys.exit(0)
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
