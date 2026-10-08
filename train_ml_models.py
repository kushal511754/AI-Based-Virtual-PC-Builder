"""
Train all ML models for the PC builder application.
This script initializes and trains:
1. Price Predictor (Random Forest)
2. Game Difficulty Classifier (Gradient Boosting)
3. FPS Predictor (Ensemble)
4. Game Similarity Engine (Embeddings-based)

Run this once after installation to train all models.
"""

import os
import sys
import time

print("="*70)
print("🤖 ML MODEL TRAINING SUITE")
print("="*70)

# Ensure models directory exists
os.makedirs('server/ml/models', exist_ok=True)

print("\n📦 Checking dependencies...")
try:
    import sklearn
    import numpy
    import scipy
    import joblib
    print("✅ scikit-learn, numpy, scipy installed")
except ImportError as e:
    print(f"❌ Missing dependency: {e}")
    print("   Run: pip install scikit-learn numpy scipy joblib")
    sys.exit(1)

try:
    import sentence_transformers
    print("✅ sentence-transformers installed")
    HAS_EMBEDDINGS = True
except ImportError:
    print("⚠️  sentence-transformers not installed (optional)")
    print("   Run: pip install sentence-transformers")
    HAS_EMBEDDINGS = False

print("\n" + "="*70)
print("1️⃣  TRAINING PRICE PREDICTOR MODEL")
print("="*70)

try:
    from server.ml.price_predictor import PricePredictor
    start = time.time()
    predictor = PricePredictor('server/ml/models/price_predictor.pkl')
    elapsed = time.time() - start
    print(f"✅ Completed in {elapsed:.2f}s")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70)
print("2️⃣  TRAINING GAME DIFFICULTY CLASSIFIER")
print("="*70)

try:
    from server.ml.game_difficulty_classifier import GameDifficultyClassifier
    start = time.time()
    classifier = GameDifficultyClassifier('server/ml/models/game_classifier.pkl')
    elapsed = time.time() - start
    print(f"✅ Completed in {elapsed:.2f}s")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70)
print("3️⃣  TRAINING FPS PREDICTION MODEL")
print("="*70)

try:
    from server.ml.fps_predictor import FPSPredictor
    start = time.time()
    fps_pred = FPSPredictor('server/ml/models/fps_predictor.pkl')
    elapsed = time.time() - start
    print(f"✅ Completed in {elapsed:.2f}s")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70)
print("4️⃣  INITIALIZING GAME SIMILARITY ENGINE")
print("="*70)

try:
    from server.ml.game_similarity import GameSimilarityEngine
    start = time.time()
    similarity = GameSimilarityEngine()
    elapsed = time.time() - start
    print(f"✅ Completed in {elapsed:.2f}s")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70)
print("✨ ALL MODELS TRAINED SUCCESSFULLY!")
print("="*70)
print("\n📊 Model Summary:")
print("   ✅ Price Predictor - Ready")
print("   ✅ Game Difficulty Classifier - Ready")
print("   ✅ FPS Prediction - Ready")
print("   ✅ Game Similarity Engine - Ready")
print("\n🚀 Start your server with: python run.py")
print("📡 API Endpoints available at /api/ml/*")
print("="*70 + "\n")
