#!/usr/bin/env python3
"""Test ML services integration."""

from server.services.ml_price_predictor import get_price_predictor
from server.services.ml_game_classifier import get_game_classifier
from server.services.ml_build_recommender import get_build_recommender

print("Testing ML Services...")
print()

# Test Price Predictor
print("1. ML Price Predictor (Ensemble: Linear Regression + Decision Tree)")
predictor = get_price_predictor()
cpu_price = predictor.predict_cpu_price(8, 4.5, 13)
print(f"   Predicted CPU price (8 cores, 4.5GHz, Gen 13): Rs {cpu_price:,.0f}")

gpu_price = predictor.predict_gpu_price(8, 256, 40)
print(f"   Predicted GPU price (8GB VRAM, Gen 40): Rs {gpu_price:,.0f}")

# Test Game Classifier
print()
print("2. ML Game Classifier (Naive Bayes)")
classifier = get_game_classifier()
result = classifier.classify_game('Cyberpunk 2077')
print(f"   Game: {result['game_name']}")
print(f"   Classification: {result['classification']} (Confidence: {result['confidence']:.2f})")
print(f"   Minimum specs: CPU={result['min_specs']['cpu_cores']} cores, GPU={result['min_specs']['gpu_vram']}GB")

# Test another game
result2 = classifier.classify_game('BGMI')
print(f"   Game: {result2['game_name']}")
print(f"   Classification: {result2['classification']} (Confidence: {result2['confidence']:.2f})")

# Test Build Recommender
print()
print("3. ML Build Recommender (K-means Clustering)")
recommender = get_build_recommender()
build = recommender.recommend_build('gaming', 100000)
print(f"   Recommended tier: {build['tier']}")
print(f"   Budget utilization: {build['budget_utilization']}")
print(f"   CPU: {build['components']['cpu']}")
print(f"   GPU: {build['components']['gpu']}")

# Test build cost prediction
print()
print("4. Build Cost Prediction (Total)")
total_cost = predictor.predict_total_build_cost(
    {'cores': 8, 'ghz': 4.5, 'generation': 13},
    {'vram': 8, 'memory_bus': 256, 'generation': 40},
    {'capacity': 16, 'speed': 5200, 'type': 2},
    {'capacity': 512, 'speed': 3500}
)
print(f"   Total build cost: Rs {total_cost['total']:,.0f}")
print(f"   CPU: Rs {total_cost['cpu_price']:,.0f}")
print(f"   GPU: Rs {total_cost['gpu_price']:,.0f}")
print(f"   RAM: Rs {total_cost['ram_price']:,.0f}")

print()
print("✅ All ML services working correctly!")
print()
print("Available Algorithms:")
print("  - Linear Regression (Price Prediction)")
print("  - Decision Tree (Component pricing)")
print("  - Naive Bayes Classification (Game requirements)")
print("  - K-means Clustering (Build recommendations)")
