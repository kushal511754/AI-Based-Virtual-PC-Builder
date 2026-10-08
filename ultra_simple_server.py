#!/usr/bin/env python
"""Ultra minimal server - no templates, no errors"""
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return '<h1>Home</h1>', 200

@app.route('/health')
def health():
    return jsonify({'status': 'ok'}), 200

# Catch ALL routes - no templates at all
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def catch_all(path):
    return f'<h1>Got request for: {path}</h1>', 200

if __name__ == '__main__':
    print("\nULTRA SIMPLE SERVER")
    print("URL: http://127.0.0.1:5000\n")
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)
