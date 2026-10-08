#!/usr/bin/env python
"""Minimal working server - guaranteed to run"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

print("\n" + "="*70)
print("MINIMAL PC SIMULATOR SERVER")
print("="*70)

try:
    from flask import Flask, jsonify, render_template
    
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static')
    
    app.config['PROPAGATE_EXCEPTIONS'] = True
    
    @app.route('/health')
    def health():
        return jsonify({'status': 'ok', 'server': 'running'}), 200
    
    @app.route('/')
    def home():
        try:
            return render_template('home.html')
        except:
            return '<html><body><h1>PC Simulator</h1><p>Server is running</p></body></html>'
    
    @app.route('/api/search/component', methods=['POST'])
    def search_component():
        from flask import request
        try:
            data = request.get_json() or {}
            query = data.get('query', 'Unknown')
            component_type = data.get('component_type', 'unknown')
            
            return jsonify({
                'success': True,
                'component': {
                    'name': query,
                    'type': component_type,
                    'price_inr': 0,
                    'price_usd': 0,
                    'source': 'minimal_server'
                }
            }), 200
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 400
    
    @app.errorhandler(Exception)
    def handle_error(e):
        return jsonify({'error': str(e)}), 500
    
    print("✓ Server initialized")
    print("✓ Listening on http://127.0.0.1:5000")
    print("="*70 + "\n")
    
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=False,
        use_reloader=False,
        threaded=True
    )

except KeyboardInterrupt:
    print("\n" + "="*70)
    print("Server stopped")
    print("="*70)
    sys.exit(0)

except Exception as e:
    print(f"\n✗ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
