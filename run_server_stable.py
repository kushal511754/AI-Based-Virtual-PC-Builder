#!/usr/bin/env python
"""Run the Flask server with better error handling"""
import os
import sys
import traceback

sys.path.insert(0, os.path.dirname(__file__))

print("=" * 60)
print("STARTING PC SIMULATOR SERVER")
print("=" * 60)

try:
    from server.app import create_app
    
    app = create_app()
    
    print("Server initialized on http://127.0.0.1:5000")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    
    # Run without redirect to prevent crashes
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=False,
        use_reloader=False,
        threaded=True,
        use_evalex=False
    )
except Exception as e:
    print(f"ERROR: {str(e)}")
    traceback.print_exc()
    sys.exit(1)
