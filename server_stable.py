#!/usr/bin/env python
"""
Stable HTTP Server - Direct Werkzeug Server (No Flask app.run() issues)
This bypasses Flask's app.run() which crashes in Windows PowerShell environment
"""
import os
import sys
import socket
from threading import Thread
import time

sys.path.insert(0, os.path.dirname(__file__))

# Minimal logging
import logging
logging.basicConfig(level=logging.CRITICAL)
for name in ['werkzeug', 'flask', 'urllib3']:
    logging.getLogger(name).setLevel(logging.CRITICAL)

def check_port_available(port):
    """Check if port is available"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        result = sock.connect_ex(('127.0.0.1', port))
        return result != 0
    finally:
        sock.close()

def start_server():
    """Start the HTTP server directly"""
    from server.app import create_app
    from werkzeug.serving import make_server
    
    app = create_app()
    
    # Create server instance (doesn't start listening yet)
    server = make_server('127.0.0.1', 5000, app, threaded=True)
    
    print("=" * 70)
    print("🚀 PC SIMULATOR SERVER - STABLE BUILD")
    print("=" * 70)
    print("✓ Application initialized")
    print("✓ Server ready on http://127.0.0.1:5000")
    print("=" * 70)
    print("\n📍 Access the application:")
    print("   🏠 Home: http://127.0.0.1:5000/")
    print("   🔍 Search API: http://127.0.0.1:5000/api/search/component")
    print("   ✓ Health Check: http://127.0.0.1:5000/health")
    print("\n💻 Press CTRL+C to stop the server")
    print("=" * 70 + "\n")
    
    sys.stdout.flush()
    
    try:
        # Start serving (this blocks)
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n✓ Server stopped gracefully")
        sys.exit(0)
    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)
    finally:
        server.shutdown()

if __name__ == '__main__':
    start_server()
