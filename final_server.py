#!/usr/bin/env python
"""
Ultimate stable server - using http.server with WSGI adapter
This is the most basic approach that should work on any system
"""
import os
import sys
import threading

sys.path.insert(0, os.path.dirname(__file__))

# Suppress logging
import logging
logging.basicConfig(level=logging.CRITICAL)
for name in ['werkzeug', 'flask', 'urllib3']:
    logging.getLogger(name).setLevel(logging.CRITICAL)

def main():
    from server.app import create_app
    from wsgiref.simple_server import make_server
    
    app = create_app()
    
    print("=" * 70)
    print("🚀 PC SIMULATOR - STABLE SERVER")
    print("=" * 70)
    print("✓ Starting on http://127.0.0.1:5000")
    print("=" * 70)
    
    # Create WSGI server
    httpd = make_server('127.0.0.1', 5000, app)
    
    print("\n📍 Access URLs:")
    print("   🏠 Home: http://127.0.0.1:5000/")
    print("   🔍 Search: http://127.0.0.1:5000/api/search/component")
    print("   ✓ Health: http://127.0.0.1:5000/health")
    print("\n💻 Server is running... Press CTRL+C to stop\n")
    print("=" * 70 + "\n")
    
    sys.stdout.flush()
    
    # Run server in thread to keep process alive
    server_thread = threading.Thread(target=httpd.serve_forever, daemon=False)
    server_thread.start()
    
    try:
        # Keep main thread alive
        while True:
            threading.Event().wait(1)
    except KeyboardInterrupt:
        print("\n✓ Server stopped")
        httpd.shutdown()
        sys.exit(0)

if __name__ == '__main__':
    main()
