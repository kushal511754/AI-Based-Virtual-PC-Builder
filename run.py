#!/usr/bin/env python
"""Main entry point for PC Builder application"""
import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.WARNING, format='%(levelname)s: %(message)s')

# Add project to path
sys.path.insert(0, os.path.dirname(__file__))

from server.app import create_app

app = create_app()
print("[OK] App created, starting Flask server...")
sys.stdout.flush()

if __name__ == '__main__':
    try:
        print("[INFO] Starting Flask development server...")
        print("[INFO] Server running at http://127.0.0.1:5000")
        print("[INFO] Login page: http://127.0.0.1:5000/login")
        print("[INFO] Opening login page in browser...")
        app.run(
            host='127.0.0.1',
            port=5000,
            debug=False,
            use_reloader=False,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n[INFO] Server stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"[ERROR] Server error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


