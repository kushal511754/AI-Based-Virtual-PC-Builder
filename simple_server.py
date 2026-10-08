#!/usr/bin/env python
"""
Minimal Flask server - direct approach
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

# Suppress all logging
import logging
logging.disable(logging.CRITICAL)

from server.app import create_app

app = create_app()

print("=" * 70)
print("🚀 PC SIMULATOR - STABLE SERVER")
print("=" * 70)
print("✓ Starting on http://127.0.0.1:5000")
print("=" * 70)
print("\n📍 Access URLs:")
print("   🏠 Home: http://127.0.0.1:5000/")
print("   🔍 Search: http://127.0.0.1:5000/api/search/component")
print("   ✓ Health: http://127.0.0.1:5000/health")
print("\n💻 Server is running... Press CTRL+C to stop\n")
print("=" * 70 + "\n")
sys.stdout.flush()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False, threaded=True)
