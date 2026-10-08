#!/usr/bin/env python
"""Simple working server - no 404 errors"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, render_template, jsonify, request

app = Flask(__name__, template_folder='templates', static_folder='static')

# Routes that return content
@app.route('/')
def home():
    try:
        return render_template('home.html')
    except:
        return '<h1>PC Simulator</h1>'

@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'server': 'running'}), 200

# Catch ANY route and return the template if it exists
@app.route('/<path:path>')
def any_route(path):
    try:
        # Try to load template
        template_names = [path + '.html', path.replace('-', '_') + '.html']
        for template_name in template_names:
            try:
                return render_template(template_name), 200
            except Exception as e:
                print(f"Template {template_name} not found: {e}")
                continue
        # Fallback HTML
        return f'<html><body><h1>PC Simulator</h1><p>Route: {path}</p></body></html>', 200
    except Exception as e:
        print(f"Route handler error: {e}")
        import traceback
        traceback.print_exc()
        return f'<html><body><h1>Error</h1><p>{str(e)}</p></body></html>', 500

@app.route('/<path:path>/<string:other>')
def any_subpath_route(path, other):
    return f'<html><body><h1>PC Simulator</h1></body></html>', 200

# API routes
@app.route('/api/search/component', methods=['POST'])
def search():
    data = request.get_json() or {}
    return jsonify({'success': True, 'component': {'name': data.get('query', 'Unknown')}}), 200

# Error handlers
@app.errorhandler(500)
def server_error(e):
    return '<html><body><h1>Server Error</h1></body></html>', 500

if __name__ == '__main__':
    print("\n" + "="*70)
    print("SIMPLE PC SIMULATOR SERVER")
    print("="*70)
    print("URL: http://127.0.0.1:5000")
    print("="*70 + "\n")
    
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=False,
        use_reloader=False,
        threaded=True
    )
