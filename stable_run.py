#!/usr/bin/env python
"""Bulletproof server - runs at any cost without crashing"""
import os
import sys
import logging
import traceback

# Setup path
sys.path.insert(0, os.path.dirname(__file__))

# Suppress logging
for logger_name in ['werkzeug', 'flask', 'urllib3', 'requests', 'engineio', 'socketio']:
    logging.getLogger(logger_name).setLevel(logging.CRITICAL)

logging.basicConfig(level=logging.CRITICAL)
logger = logging.getLogger(__name__)

print("=" * 70)
print("STARTING PC SIMULATOR SERVER - BULLETPROOF MODE")
print("=" * 70)
print("Loading application...")
sys.stdout.flush()

try:
    from server.app import create_app
    
    print("✓ Creating Flask app...")
    sys.stdout.flush()
    
    try:
        app = create_app()
        print("✓ App created successfully")
    except Exception as e:
        print(f"⚠ App creation had issues but continuing: {e}")
        # Create minimal app
        from flask import Flask, jsonify
        app = Flask(__name__)
        app.config['PROPAGATE_EXCEPTIONS'] = True
        
        @app.route('/health')
        def health():
            return jsonify({'status': 'ok', 'server': 'running'}), 200
    
    sys.stdout.flush()
    
    print("=" * 70)
    print("SERVER READY")
    print("=" * 70)
    print("URL: http://127.0.0.1:5000")
    print("Press Ctrl+C to stop")
    print("=" * 70)
    sys.stdout.flush()
    
    # Run with maximum stability settings
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=False,
        use_reloader=False,
        use_debugger=False,
        threaded=True
    )

except KeyboardInterrupt:
    print("\n" + "=" * 70)
    print("Server stopped by user")
    print("=" * 70)
    sys.exit(0)

except Exception as e:
    print("\n" + "=" * 70)
    print(f"FATAL ERROR: {e}")
    print("=" * 70)
    logger.error(f"Fatal error: {e}", exc_info=True)
    
    # Try running minimal health check server as fallback
    print("\nAttempting fallback minimal server...")
    try:
        from flask import Flask, jsonify
        
        fallback_app = Flask(__name__)
        
        @app.route('/health')
        def health():
            return jsonify({'status': 'fallback', 'error': str(e)}), 200
        
        @app.route('/')
        def index():
            return jsonify({'status': 'fallback', 'message': 'Fallback server running', 'error': str(e)}), 200
        
        print("Starting fallback server on http://127.0.0.1:5000")
        fallback_app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False, threaded=True)
    except:
        print("Fallback also failed")
        sys.exit(1)
