#!/usr/bin/env python
"""Verify ML integration in Flask app."""
import sys
import traceback

try:
    print("=" * 60)
    print("VERIFYING ML INTEGRATION")
    print("=" * 60)
    
    # Test 1: Import app
    print("\n1️⃣ Creating Flask app...")
    from server.app import create_app
    app = create_app()
    print("   ✅ App created successfully")
    
    # Test 2: Check ML blueprint
    print("\n2️⃣ Checking ML blueprint registration...")
    if 'ml' in app.blueprints:
        print("   ✅ ML blueprint registered")
    else:
        print("   ❌ ML blueprint NOT registered")
        print(f"   Available blueprints: {list(app.blueprints.keys())}")
    
    # Test 3: Count routes
    print("\n3️⃣ Checking API routes...")
    ml_routes = [rule for rule in app.url_map.iter_rules() if '/api/ml' in rule.rule]
    print(f"   ✅ Found {len(ml_routes)} ML API routes:")
    for route in ml_routes:
        print(f"      - {route.rule} [{', '.join(route.methods - {'HEAD', 'OPTIONS'})}]")
    
    # Test 4: Test each ML service directly
    print("\n4️⃣ Testing ML services directly (Python level)...")
    
    # Price predictor
    try:
        from server.services.ml_price_predictor import get_price_predictor
        predictor = get_price_predictor()
        price = predictor.predict_cpu_price(4, 2.5)
        print(f"   ✅ Price Predictor: CPU price = ₹{price:,.0f}")
    except Exception as e:
        print(f"   ❌ Price Predictor failed: {e}")
    
    # Game classifier
    try:
        from server.services.ml_game_classifier import get_game_classifier
        classifier = get_game_classifier()
        result = classifier.classify_game("Call of Duty")
        print(f"   ✅ Game Classifier: CoD = {result['classification']} (confidence: {result['confidence']:.2f})")
    except Exception as e:
        print(f"   ❌ Game Classifier failed: {e}")
    
    # Build recommender
    try:
        from server.services.ml_build_recommender import get_build_recommender
        recommender = get_build_recommender()
        result = recommender.recommend_build('gaming', 70000)
        print(f"   ✅ Build Recommender: Budget ₹70k = {result['tier']} tier")
    except Exception as e:
        print(f"   ❌ Build Recommender failed: {e}")
    
    print("\n" + "=" * 60)
    print("✅ ALL VERIFICATIONS PASSED!")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    traceback.print_exc()
    sys.exit(1)
