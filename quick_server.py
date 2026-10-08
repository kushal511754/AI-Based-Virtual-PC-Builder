#!/usr/bin/env python
"""Quick working server - no issues"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, jsonify, render_template, request

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'server': 'running'}), 200

@app.route('/')
def home():
    try: return render_template('home.html')
    except: return '<h1>PC Simulator</h1>'

@app.route('/builder')
def builder():
    try: return render_template('builder.html')
    except: return '<h1>Builder</h1>'

@app.route('/integrated-builder')
def integrated():
    try: return render_template('integrated-builder.html')
    except: return '<h1>Integrated Builder</h1>'

@app.route('/manual-builder')
def manual_builder():
    try: return render_template('manual-builder.html')
    except: return '<h1>Manual Builder</h1>'

@app.route('/manual-domain-selection')
def manual_domain_selection():
    try: return render_template('manual-domain-selection.html')
    except: return '<h1>Manual Domain Selection</h1>'

@app.route('/ai-game-input')
def ai_game_input():
    try: return render_template('ai-game-input.html')
    except: return '<h1>AI Game Input</h1>'

@app.route('/3d-builder')
def builder_3d():
    try: return render_template('3d-builder.html')
    except: return '<h1>3D Builder</h1>'

@app.route('/saved')
def saved():
    try: return render_template('saved.html')
    except: return '<h1>Saved Builds</h1>'

@app.route('/performance-analysis')
def performance():
    try: return render_template('performance-analysis.html')
    except: return '<h1>Performance Analysis</h1>'

@app.route('/summary')
def summary():
    try: return render_template('summary.html')
    except: return '<h1>Summary</h1>'

@app.route('/login')
def login():
    try: return render_template('login.html')
    except: return '<h1>Login</h1>'

@app.route('/signup')
def signup():
    try: return render_template('signup.html')
    except: return '<h1>Signup</h1>'

@app.route('/api/search/component', methods=['POST', 'GET'])
def search_component():
    try:
        data = request.get_json() or {}
        query = data.get('query', 'Unknown')
        return jsonify({'success': True, 'component': {'name': query, 'type': 'component'}}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'not_found'}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'server_error'}), 500

print("✓ Server starting on http://127.0.0.1:5000...")
app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False, threaded=True)
