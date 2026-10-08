#!/usr/bin/env python
"""Simple HTTP server that works - uses Flask test client internally"""
import sys
import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import time

sys.path.insert(0, os.path.dirname(__file__))

from server.app import create_app

# Create app once at startup
main_app = create_app()

class RequestHandler(BaseHTTPRequestHandler):
    """HTTP request handler using Flask test client"""
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'ok'}).encode())
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Not found'}).encode())
    
    def do_POST(self):
        """Handle POST requests"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body) if body else {}
            
            # Route to correct endpoint
            if self.path == '/api/search/component':
                try:
                    with main_app.test_client() as client:
                        resp = client.post('/api/search/component', json=data)
                        result = resp.get_json()
                        status = resp.status_code
                except Exception as inner_e:
                    result = {'success': False, 'error': str(inner_e)}
                    status = 500
            else:
                result = {'error': 'Not found'}
                status = 404
            
            # Send response
            self.send_response(status)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response_bytes = json.dumps(result).encode()
            self.wfile.write(response_bytes)
            
        except Exception as e:
            try:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())
            except:
                pass
    
    def log_message(self, format, *args):
        """Suppress logging"""
        pass

def run_server():
    """Run the HTTP server"""
    try:
        server = HTTPServer(('127.0.0.1', 5000), RequestHandler)
        server.timeout = 5
        while True:
            try:
                server.handle_request()
            except KeyboardInterrupt:
                raise
            except Exception as e:
                pass
    except KeyboardInterrupt:
        pass
    finally:
        try:
            server.server_close()
        except:
            pass

if __name__ == '__main__':
    print("=" * 70)
    print("PC SIMULATOR - GLOBAL SEARCH")
    print("=" * 70)
    print("\n✓ Server running at: http://127.0.0.1:5000\n")
    print("API Endpoints:")
    print("  • POST /api/search/component - Search for PC components")
    print("  • GET  /health - Health check")
    print("\nExample request:")
    print('  curl -X POST http://127.0.0.1:5000/api/search/component \\')
    print('    -H "Content-Type: application/json" \\')
    print('    -d \'{"query":"MSI B450 Tomahawk (AM4)","component_type":"motherboard"}\'')
    print("\n" + "=" * 70)
    print("Press Ctrl+C to stop\n")
    
    try:
        run_server()
    except KeyboardInterrupt:
        print("\n\nServer stopped")
        sys.exit(0)
