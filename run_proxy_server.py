#!/usr/bin/env python
"""Flask server using test client proxy to avoid HTTP crashing issues"""
import sys
import os
from threading import Thread
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

sys.path.insert(0, os.path.dirname(__file__))

from server.app import create_app

# Create the main app once
main_app = create_app()

class ProxyHandler(BaseHTTPRequestHandler):
    """HTTP handler that uses Flask test client internally"""
    
    def do_POST(self):
        """Handle POST requests via test client"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            
            # Parse JSON
            try:
                data = json.loads(body)
            except:
                data = {}
            
            # Use test client to handle the request
            with main_app.test_client() as client:
                if self.path == '/api/search/component':
                    resp = client.post('/api/search/component', json=data)
                    response_data = resp.get_json()
                    status_code = resp.status_code
                else:
                    response_data = {'error': 'Not found'}
                    status_code = 404
            
            # Send response
            self.send_response(status_code)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            error_response = json.dumps({'error': str(e)})
            self.wfile.write(error_response.encode('utf-8'))
    
    def do_GET(self):
        """Handle GET requests"""
        try:
            with main_app.test_client() as client:
                if self.path == '/health':
                    resp = client.get('/health')
                    response_data = resp.get_json()
                    status_code = resp.status_code
                else:
                    response_data = {'error': 'Not found'}
                    status_code = 404
            
            self.send_response(status_code)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            error_response = json.dumps({'error': str(e)})
            self.wfile.write(error_response.encode('utf-8'))
    
    def log_message(self, format, *args):
        """Suppress logging"""
        pass

if __name__ == '__main__':
    print("=" * 60)
    print("PC SIMULATOR SERVER (Proxy Mode)")
    print("=" * 60)
    print("Server running on http://127.0.0.1:5000")
    print("=" * 60)
    
    # Start HTTP server
    server = HTTPServer(('127.0.0.1', 5000), ProxyHandler)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")
        sys.exit(0)
