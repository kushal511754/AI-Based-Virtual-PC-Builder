#!/usr/bin/env python
"""Minimal server to test if issue is in Flask or app.py"""
from flask import Flask, render_template
import traceback
import sys

app = Flask(__name__, template_folder='templates')

@app.route('/')
def home():
    return '<h1>Home</h1>'

@app.route('/manual-domain-selection')
def manual():
    try:
        return render_template('manual-domain-selection.html')
    except Exception as e:
        print(f"TEMPLATE ERROR: {e}")
        traceback.print_exc()
        sys.stdout.flush()
        return f'<h1>Error</h1><p>{str(e)}</p>', 500

@app.route('/<path:path>')
def catchall(path):
    try:
        return render_template(f'{path}.html')
    except:
        return f'<h1>Page</h1>', 200

if __name__ == '__main__':
    print("TEST SERVER STARTING")
    try:
        app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)
    except Exception as e:
        print(f"FATAL: {e}")
        traceback.print_exc()
        sys.exit(1)
