#!/usr/bin/env python
"""
PC Simulator - Works perfectly with test client
Just run: python quick_search.py <component_query>
"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from server.app import create_app

def search(query, comp_type=""):
    """Search for a component"""
    app = create_app()
    
    with app.test_client() as client:
        resp = client.post('/api/search/component', json={
            'query': query,
            'component_type': comp_type
        })
        return resp.get_json()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("=" * 70)
        print("PC SIMULATOR - GLOBAL SEARCH")
        print("=" * 70)
        print("\nUsage: python quick_search.py '<component_name>'")
        print("\nExamples:")
        print("  python quick_search.py 'MSI B450 Tomahawk (AM4)'")
        print("  python quick_search.py 'RTX 4070'")
        print("  python quick_search.py 'Ryzen 9 7950X'")
        print("\n" + "=" * 70)
        sys.exit(0)
    
    query = ' '.join(sys.argv[1:])
    
    print("\n" + "=" * 70)
    print(f"Searching for: {query}")
    print("=" * 70 + "\n")
    
    result = search(query)
    
    if result.get('success'):
        comp = result['component']
        print(f"✓ FOUND!\n")
        print(f"  Name:      {comp['name']}")
        print(f"  Type:      {comp['type']}")
        print(f"  Price INR: Rs.{comp['price_inr']}")
        print(f"  Price USD: ${comp['price_usd']}")
        if comp.get('socket'):
            print(f"  Socket:    {comp['socket']}")
        if comp.get('retailers'):
            print(f"  Retailers: {len(comp['retailers'])}")
    else:
        print(f"✗ Not found: {result.get('error')}")
    
    print("\n" + "=" * 70)
