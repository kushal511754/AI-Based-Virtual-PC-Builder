#!/usr/bin/env python
"""Run the Flask server with maximum stability"""
import os
import sys
import logging
import traceback

# Setup path
sys.path.insert(0, os.path.dirname(__file__))

# Suppress all verbose logging
for logger_name in ['werkzeug', 'flask', 'urllib3', 'requests']:
    logging.getLogger(logger_name).setLevel(logging.CRITICAL)

logging.basicConfig(level=logging.CRITICAL)

print("=" * 60)
print("STARTING PC SIMULATOR SERVER")
print("=" * 60)

try:
    from server.app import create_app
    app = create_app()
    
    # Wrap EVERY route to catch exceptions
    original_dispatch_request = app.dispatch_request
    
    def safe_dispatch_request():
        try:
            return original_dispatch_request()
        except Exception as e:
            print(f"DISPATCH ERROR: {e}", flush=True)
            traceback.print_exc()
            sys.stdout.flush()
            from flask import jsonify
            return jsonify({'error': str(e)}), 500
    
    app.dispatch_request = safe_dispatch_request
    
    print("Server initialized on http://127.0.0.1:5000")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    
    # Run with minimal options for stability
    print("Starting Flask app.run()...")
    sys.stdout.flush()
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=False,
        use_reloader=False,
        use_debugger=False,
        threaded=True
    )
except KeyboardInterrupt:
    print("\nServer stopped")
    sys.exit(0)
except Exception as e:
    print(f"ERROR: {e}", flush=True)
    traceback.print_exc()
    sys.stdout.flush()
    sys.exit(1)
