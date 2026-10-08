"""
Test ML models and API endpoints.
Verifies all machine learning models are working correctly.
"""

import json
import requests
import time

print("="*70)
print("🧪 ML MODELS & API TEST SUITE")
print("="*70)

# Test data
TEST_CASES = {
    'price_prediction': {
        'url': 'http://localhost:5000/api/ml/predict-price',
        'data': {
            'component_type': 'gpu',
            'cores_or_vram': 16,
            'clock_speed': 2.0,
            'days_old': 150
        },
        'description': '💰 GPU Price Prediction'
    },
    'game_difficulty': {
        'url': 'http://localhost:5000/api/ml/game-difficulty',
        'data': {
            'game_name': 'Cyberpunk 2077',
            'min_ram_gb': 16,
            'min_vram_gb': 8,
            'min_cpu_cores': 8
        },
        'description': '🎮 Game Difficulty Classification'
    },
    'fps_prediction': {
        'url': 'http://localhost:5000/api/ml/predict-fps',
        'data': {
            'game_name': 'Cyberpunk 2077',
            'game_min_ram': 16,
            'game_min_vram': 8,
            'game_min_cores': 8,
            'pc_ram': 32,
            'pc_vram': 16,
            'pc_cores': 16
        },
        'description': '📊 FPS Prediction'
    },
    'similar_games': {
        'url': 'http://localhost:5000/api/ml/similar-games',
        'data': {
            'game_name': 'BGMI',
            'top_k': 3
        },
        'description': '🔍 Similar Games Search'
    },
    'game_search': {
        'url': 'http://localhost:5000/api/ml/game-search',
        'data': {
            'query': 'Games like BGMI'
        },
        'description': '🎯 Semantic Game Search'
    },
    'build_analysis': {
        'url': 'http://localhost:5000/api/ml/analyze-build',
        'data': {
            'game_name': 'Cyberpunk 2077',
            'pc_specs': {
                'cpu_cores': 16,
                'cpu_name': 'Intel i9-13900K',
                'gpu_vram': 16,
                'gpu_name': 'RTX 4080',
                'ram_gb': 32
            }
        },
        'description': '🏗️ Comprehensive Build Analysis'
    },
    'ml_status': {
        'url': 'http://localhost:5000/api/ml/status',
        'data': None,
        'description': '📈 ML Models Status',
        'method': 'GET'
    }
}

def test_endpoint(name, test_info):
    """Test a single endpoint."""
    method = test_info.get('method', 'POST')
    url = test_info['url']
    data = test_info.get('data')
    description = test_info['description']
    
    print(f"\n{description}")
    print(f"{'─'*70}")
    
    try:
        if method == 'GET':
            response = requests.get(url, timeout=10)
        else:
            response = requests.post(url, json=data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Status: {response.status_code}")
            print(f"📦 Response: {json.dumps(result, indent=2)}")
            return True
        else:
            print(f"❌ Status: {response.status_code}")
            print(f"📦 Response: {response.text}")
            return False
    
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error - Is the Flask server running?")
        print("   Run: python run.py")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all tests."""
    print("\n⏳ Testing ML API endpoints...")
    print("   Make sure Flask server is running: python run.py\n")
    
    time.sleep(1)
    
    results = {}
    
    for test_name, test_info in TEST_CASES.items():
        results[test_name] = test_endpoint(test_name, test_info)
    
    # Summary
    print("\n" + "="*70)
    print("📊 TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, passed_flag in results.items():
        status = "✅ PASS" if passed_flag else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\n{'='*70}")
    print(f"Results: {passed}/{total} tests passed")
    print("="*70 + "\n")
    
    if passed == total:
        print("🎉 All tests passed! ML models are working correctly.")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
    
    return passed == total

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
