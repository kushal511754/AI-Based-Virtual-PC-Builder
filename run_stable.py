#!/usr/bin/env python
"""Run the AIPCSimulator Flask app - Stable Version"""
import os
import sys
import logging

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(__file__))

# Suppress all Werkzeug and Flask logging
logging.getLogger('werkzeug').setLevel(logging.CRITICAL)
logging.getLogger('flask').setLevel(logging.CRITICAL)
logging.getLogger('flask.app').setLevel(logging.CRITICAL)

# Setup minimal console logging
logging.basicConfig(
    level=logging.CRITICAL,
    format='%(message)s'
)

def main():
    try:
        print("=" * 60)
        print("Initializing Flask Application...")
        print("=" * 60)
        
        from server.app import create_app
        app = create_app()
        
        print("✓ Flask app created successfully")
        print("=" * 60)
        print("✓ Starting Server on http://127.0.0.1:5000")
        print("  Press CTRL+C to stop")
        print("=" * 60)
        
        # Suppress Werkzeug output
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)
        
        # Run Flask
        app.run(
            debug=False,
            host='127.0.0.1',
            port=5000,
            use_reloader=False,
            threaded=True,
            use_debugger=False
        )
    except KeyboardInterrupt:
        print("\n✓ Server shutting down...")
        sys.exit(0)
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
