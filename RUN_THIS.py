#!/usr/bin/env python
"""
MINIMAL WSGI SERVER - NO FLASK CRASHES
Direct WSGI implementation - bypasses all Flask/Werkzeug issues
"""
import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

# ===== MINIMAL COMPONENT SEARCH (NO IMPORTS) =====
COMPONENTS_DB = {
    'MSI B450 TOMAHAWK': {
        'name': 'MSI B450 TOMAHAWK (AM4)',
        'type': 'motherboard',
        'socket': 'AM4',
        'chipset': 'B450',
        'form': 'ATX',
        'price_inr': 15599,
        'price_usd': 189,
        'retailers': ['Amazon.in', 'Flipkart']
    }
}

def search_component(query, comp_type):
    """Search component from minimal DB"""
    query_upper = query.upper()
    for key, comp in COMPONENTS_DB.items():
        if key in query_upper or query_upper in key:
            return {'success': True, 'component': comp}
    return {'success': False, 'error': 'Component not found'}

# ===== MINIMAL WSGI APP =====
def app(environ, start_response):
    """Minimal WSGI application - NO FLASK"""
    path = environ.get('PATH_INFO', '/')
    method = environ.get('REQUEST_METHOD', 'GET')
    
    # Health endpoint
    if path == '/health' and method == 'GET':
        response = json.dumps({'status': 'ok', 'server': 'running'})
        start_response('200 OK', [('Content-Type', 'application/json')])
        return [response.encode()]
    
    # Component search endpoint
    if path == '/api/search/component' and method == 'POST':
        try:
            content_length = int(environ.get('CONTENT_LENGTH', 0))
            body = environ['wsgi.input'].read(content_length).decode()
            data = json.loads(body)
            query = data.get('query', '')
            comp_type = data.get('component_type', '')
            
            result = search_component(query, comp_type)
            response = json.dumps(result)
            start_response('200 OK', [('Content-Type', 'application/json')])
            return [response.encode()]
        except Exception as e:
            response = json.dumps({'success': False, 'error': str(e)})
            start_response('500 Internal Server Error', [('Content-Type', 'application/json')])
            return [response.encode()]
    
    # 404
    response = json.dumps({'error': 'Not found'})
    start_response('404 Not Found', [('Content-Type', 'application/json')])
    return [response.encode()]

# ===== RUN SERVER =====
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    
    print("[*] MINIMAL WSGI SERVER")
    print("[*] http://127.0.0.1:5000/")
    print("[*] /health - Health check")
    print("[*] /api/search/component - Search (POST)")
    sys.stdout.flush()
    
    httpd = make_server('127.0.0.1', 5000, app)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()
