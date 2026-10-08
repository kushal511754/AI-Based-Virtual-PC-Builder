#!/usr/bin/env python
"""Quick test to verify the manual builder fixes work"""
import sys
sys.path.insert(0, '.')

from server.app import create_app

# Create app
app = create_app()

# Add test route
@app.route('/test-click-search')
def test_click_search():
    """Serve test page"""
    with open('templates/test_click_search.html', 'r') as f:
        return f.read()

if __name__ == '__main__':
    print("\n" + "="*70)
    print("Testing Click & Search Functionality")
    print("="*70)
    print("\nOpen browser to: http://127.0.0.1:5000/test-click-search")
    print("\nTo test the actual manual builder:")
    print("1. Go to: http://127.0.0.1:5000/manual-domain-selection")
    print("2. Select a domain (Gaming, Streaming, etc)")
    print("3. Enter a game/goal name")
    print("4. Click 'Continue'")
    print("5. Click any 'Quick Add' button to open modal")
    print("6. Try searching (e.g., type 'intel')")
    print("7. Try clicking a component")
    print("\n" + "="*70)
    
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False, threaded=True)
