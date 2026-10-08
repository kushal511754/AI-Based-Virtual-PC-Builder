#!/usr/bin/env python
"""Simple working server - NO factory pattern"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, render_template, jsonify, request

print("\n" + "="*70)
print("STARTING PC SIMULATOR SERVER - SIMPLE MODE")
print("="*70 + "\n")

app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')

# ============ ALL ROUTES HERE ============
@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'server': 'running'}), 200

@app.route('/')
def home():
    try:
        return render_template('home.html')
    except:
        return '<h1>PC Simulator</h1>'

@app.route('/builder')
def builder():
    try:
        return render_template('builder.html')
    except:
        return '<h1>Builder</h1>'

@app.route('/integrated-builder')
def integrated_builder():
    try:
        return render_template('integrated-builder.html')
    except:
        return '<h1>Integrated Builder</h1>'

@app.route('/manual-domain-selection')
def manual_domain_selection():
    try:
        return render_template('manual-domain-selection.html')
    except:
        return '<h1>Manual Domain Selection</h1>'

@app.route('/manual-builder')
def manual_builder():
    try:
        return render_template('manual-builder.html')
    except:
        return '<h1>Manual Builder</h1>'

@app.route('/3d-builder')
def builder_3d():
    try:
        return render_template('3d-builder.html')
    except:
        return '<h1>3D Builder</h1>'

@app.route('/saved')
def saved_builds():
    try:
        return render_template('saved.html')
    except:
        return '<h1>Saved Builds</h1>'

@app.route('/ai-game-input')
def ai_game():
    try:
        return render_template('ai-game-input.html')
    except:
        return '<h1>AI Game Input</h1>'

@app.route('/login')
def login():
    try:
        return render_template('login.html')
    except:
        return '<h1>Login</h1>'

@app.route('/signup')
def signup():
    try:
        return render_template('signup.html')
    except:
        return '<h1>Signup</h1>'

@app.route('/api/search/component', methods=['POST', 'GET'])
def search_component():
    try:
        if request.method == 'GET':
            query = request.args.get('query', '')
        else:
            data = request.get_json() or {}
            query = data.get('query', '')
        
        return jsonify({
            'success': True,
            'component': {'name': query}
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'not_found'}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'server_error'}), 500

print("✓ All routes registered")
print("="*70)
print("✓ SERVER READY")
print("URL: http://127.0.0.1:5000")
print("="*70 + "\n")

if __name__ == '__main__':
    try:
        app.run(
            host='127.0.0.1',
            port=5000,
            debug=False,
            use_reloader=False,
            use_debugger=False,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n" + "="*70)
        print("Server stopped")
        print("="*70)
        sys.exit(0)
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
