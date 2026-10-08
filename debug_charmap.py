#!/usr/bin/env python
"""Debug the charmap error."""
import sys
sys.path.insert(0, '.')

try:
    from server.services.ml_price_predictor import get_price_predictor
    predictor = get_price_predictor()
    print("Price predictor loaded")
    
    # Try to serialize it to JSON
    import json
    result = {
        'status': 'Ready',
        'ml_services': {
            'price_predictor': 'Ready' if predictor.models_trained else 'Not trained',
            'game_classifier': 'Ready',
            'build_recommender': 'Ready'
        },
        'algorithms': ['Linear Regression', 'Decision Tree', 'Naive Bayes Classification', 'K-means Clustering'],
        'endpoints': ['/api/ml/predict-component-price', '/api/ml/predict-build-cost']
    }
    
    json_str = json.dumps(result, ensure_ascii=True)
    print("JSON serialization successful")
    print(json_str)
    
except Exception as e:
    import traceback
    print(f"Error: {e}")
    traceback.print_exc()
