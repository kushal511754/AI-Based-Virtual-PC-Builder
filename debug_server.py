#!/usr/bin/env python
import sys
import traceback
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return 'HOME', 200

@app.route('/health')
def health():
    return 'OK', 200

@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
    return f'PATH: {path}', 200

@app.before_request
def before():
    print(f"Request: {request.method} {request.path}", flush=True)

@app.after_request
def after(response):
    print(f"Response: {response.status_code}", flush=True)
    return response

@app.errorhandler(Exception)
def handle_error(e):
    print(f"ERROR: {e}", flush=True)
    traceback.print_exc()
    return 'ERROR', 500

if __name__ == '__main__':
    print("SERVER STARTING\n", flush=True)
    try:
        app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)
    except Exception as e:
        print(f"FATAL: {e}", flush=True)
        traceback.print_exc()
        sys.exit(1)
