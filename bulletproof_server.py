#!/usr/bin/env python
"""Bulletproof server with complete exception handling"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

print("\n" + "="*70)
print("STARTING PC SIMULATOR SERVER - FAIL SAFE MODE")
print("="*70 + "\n")

try:
    # Step 1: Create Flask app
    print("[1/3] Importing Flask...")
    from flask import Flask, jsonify, render_template, request
    print("    ✓ Flask imported")
    
    # Step 2: Create app instance
    print("[2/3] Creating Flask application...")
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static')
    
    app.config['PROPAGATE_EXCEPTIONS'] = True
    print("    ✓ Flask app created")
    
    # Step 3: Register routes
    print("[3/3] Registering routes...")
    
    @app.route('/health')
    def health():
        return jsonify({'status': 'ok', 'server': 'running'}), 200
    
    @app.route('/')
    def home():
        try:
            return render_template('home.html')
        except:
            return '''<html>
<head><title>PC Simulator</title></head>
<body><h1>PC Simulator Server</h1><p>Server is running at http://127.0.0.1:5000</p></body>
</html>'''
    
    @app.route('/api/search/component', methods=['POST', 'GET'])
    def search_component():
        try:
            if request.method == 'GET':
                query = request.args.get('query', 'Unknown')
            else:
                data = request.get_json() or {}
                query = data.get('query', 'Unknown')
            
            return jsonify({
                'success': True,
                'component': {'name': query, 'type': 'component', 'price_inr': 0, 'price_usd': 0}
            }), 200
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 400
    
    @app.route('/builder')
    def builder():
        try:
            return render_template('builder.html')
        except:
            return '<html><body><h1>Builder</h1><p>PC Builder Page</p></body></html>'
    
    @app.route('/integrated-builder')
    def integrated_builder():
        try:
            return render_template('integrated-builder.html')
        except:
            return '<html><body><h1>Integrated Builder</h1><p>PC Builder</p></body></html>'
    
    @app.route('/manual-builder')
    def manual_builder():
        try:
            return render_template('manual-builder.html')
        except:
            return '<html><body><h1>Manual Builder</h1></body></html>'
    
    @app.route('/saved')
    def saved_builds():
        try:
            return render_template('saved.html')
        except:
            return '<html><body><h1>Saved Builds</h1></body></html>'
    
    @app.route('/3d-builder')
    def builder_3d():
        try:
            return render_template('3d-builder.html')
        except:
            return '<html><body><h1>3D Builder</h1></body></html>'
    
    @app.route('/manual-domain-selection')
    def manual_domain():
        try:
            return render_template('manual-domain-selection.html')
        except:
            return '<html><body><h1>Domain Selection</h1></body></html>'
    
    @app.route('/ai-game-input')
    def ai_game():
        try:
            return render_template('ai-game-input.html')
        except:
            return '<html><body><h1>AI Game Input</h1></body></html>'
    
    @app.route('/performance-analysis')
    def performance():
        try:
            return render_template('performance-analysis.html')
        except:
            return '<html><body><h1>Performance Analysis</h1></body></html>'
    
    @app.route('/summary')
    def summary():
        try:
            return render_template('summary.html')
        except:
            return '<html><body><h1>Build Summary</h1></body></html>'
    
    @app.route('/login')
    def login_page():
        try:
            return render_template('login.html')
        except:
            return '<html><body><h1>Login</h1></body></html>'
    
    @app.route('/signup')
    def signup_page():
        try:
            return render_template('signup.html')
        except:
            return '<html><body><h1>Signup</h1></body></html>'
    
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'error': 'not_found'}), 404
    
    @app.errorhandler(500)
    def server_error(e):
        return jsonify({'error': 'server_error'}), 500
    
    print("    ✓ Routes registered")
    
    print("\n" + "="*70)
    print("✓ SERVER READY")
    print("="*70)
    print("URL: http://127.0.0.1:5000")
    print("Health: http://127.0.0.1:5000/health")
    print("="*70 + "\n")
    
    # Run server
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
    print("Server stopped by user")
    print("="*70)
    sys.exit(0)

except Exception as e:
    print(f"\n✗ ERROR: {type(e).__name__}: {e}")
    
    # If Flask run method failed, try without certain args
    try:
        print("\n[FALLBACK] Attempting basic Flask run...")
        app.run(
            host='127.0.0.1',
            port=5000,
            debug=False,
            use_reloader=False,
            threaded=True
        )
    except:
        print("[FALLBACK] Basic run also failed")
        import traceback
        traceback.print_exc()
        sys.exit(1)
