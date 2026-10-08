#!/usr/bin/env python
"""
PC Component Search - Direct Browser Interface
Uses Flask internally without HTTP complications
"""
import sys
import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import webbrowser
import time
import threading

sys.path.insert(0, os.path.dirname(__file__))

from server.app import create_app

# Create app once
app = create_app()

class SimpleHandler(BaseHTTPRequestHandler):
    """Simple HTTP handler with proper error handling"""
    
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        """Serve HTML interface"""
        if self.path == '/':
            html = open('templates/search.html', 'r').read() if os.path.exists('templates/search.html') else self.get_default_html()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode())
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status":"ok"}')
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"error":"Not found"}')
    
    def do_POST(self):
        """Handle search requests"""
        if self.path == '/api/search':
            try:
                length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(length).decode()
                data = json.loads(body)
                
                query = data.get('query', '').strip()
                comp_type = data.get('type', '').strip().lower()
                
                # Use Flask test client
                with app.test_client() as client:
                    resp = client.post('/api/search/component', 
                                     json={'query': query, 'component_type': comp_type})
                    result = resp.get_json()
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(result).encode())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e), 'success': False}).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"error":"Not found"}')
    
    def get_default_html(self):
        """Default HTML interface"""
        return '''<!DOCTYPE html>
<html>
<head>
    <title>PC Component Search</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; }
        input, button { padding: 10px; font-size: 16px; }
        button { background: #4CAF50; color: white; border: none; cursor: pointer; }
        .result { background: #f0f0f0; padding: 20px; margin-top: 20px; border-radius: 5px; }
        .error { color: red; }
        .success { color: green; }
    </style>
</head>
<body>
    <h1>🔍 PC Component Search</h1>
    <input type="text" id="query" placeholder="Search component (e.g., MSI B450 Tomahawk (AM4))" style="width: 100%; padding: 10px;">
    <button onclick="search()">Search</button>
    <div id="result"></div>
    
    <script>
        async function search() {
            const query = document.getElementById('query').value;
            const result = document.getElementById('result');
            
            if (!query) {
                result.innerHTML = '<p class="error">Please enter a search query</p>';
                return;
            }
            
            result.innerHTML = '<p>Searching...</p>';
            
            try {
                const response = await fetch('/api/search', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query: query, type: '' })
                });
                
                const data = await response.json();
                
                if (data.success && data.component) {
                    const c = data.component;
                    result.innerHTML = `
                        <div class="result success">
                            <h3>${c.name}</h3>
                            <p><strong>Type:</strong> ${c.type}</p>
                            <p><strong>Price:</strong> Rs.${c.price_inr} / $${c.price_usd}</p>
                            ${c.socket ? '<p><strong>Socket:</strong> ' + c.socket + '</p>' : ''}
                            <p><strong>Retailers:</strong> ${c.retailers ? c.retailers.length : 0}</p>
                        </div>
                    `;
                } else {
                    result.innerHTML = '<p class="error">Component not found: ' + (data.error || 'Unknown error') + '</p>';
                }
            } catch (err) {
                result.innerHTML = '<p class="error">Error: ' + err.message + '</p>';
            }
        }
        
        // Allow Enter key
        document.getElementById('query').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') search();
        });
    </script>
</body>
</html>'''
    
    def log_message(self, format, *args):
        pass

if __name__ == '__main__':
    print("=" * 70)
    print("PC SIMULATOR - GLOBAL SEARCH ENGINE")
    print("=" * 70)
    print("\n✓ Server running on http://127.0.0.1:5000\n")
    
    server = HTTPServer(('127.0.0.1', 5000), SimpleHandler)
    
    print("Press Ctrl+C to stop\n")
    print("=" * 70)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\nServer stopped")
        sys.exit(0)
