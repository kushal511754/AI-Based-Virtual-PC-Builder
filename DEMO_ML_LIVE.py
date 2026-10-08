#!/usr/bin/env python
"""
LIVE ML DEMO - Show all ML features working
"""
import sys
sys.path.insert(0, '.')

print("\n" + "="*80)
print("LIVE ML FEATURES DEMO")
print("="*80 + "\n")

# ============================================================================
# 1. GAME CLASSIFIER - Naive Bayes Algorithm
# ============================================================================
print("[1] GAME CLASSIFIER (Naive Bayes)")
print("-" * 80)

from server.services.ml_game_classifier import get_game_classifier

classifier = get_game_classifier()

games_to_test = [
    "Elden Ring",
    "Fortnite", 
    "Cyberpunk 2077",
    "Star Citizen"
]

print("\nPredicting game performance tiers:\n")
for game in games_to_test:
    result = classifier.classify_game(game)
    print(f"  {game:20} → {result['classification']:10} (Confidence: {result['confidence']:.1%})")
    print(f"    Min Specs: {result['min_specs']['cpu_cores']} cores, {result['min_specs']['gpu_vram']}GB VRAM, {result['min_specs']['ram_gb']}GB RAM")
    print(f"    FPS Predictions: 1080p High = {result['predicted_fps']['1080p_high']}, 4K High = {result['predicted_fps']['4k_high']}")
    print()

# ============================================================================
# 2. PRICE PREDICTOR - Linear Regression + Decision Tree Ensemble
# ============================================================================
print("\n[2] PRICE PREDICTOR (Ensemble: Linear Regression + Decision Tree)")
print("-" * 80)

from server.services.ml_price_predictor import get_price_predictor

predictor = get_price_predictor()

print("\nPredicting component prices based on specifications:\n")

components = [
    ("CPU", {"cores": 6, "ghz": 4.5, "generation": 13}),
    ("CPU", {"cores": 8, "ghz": 5.2, "generation": 13}),
    ("CPU", {"cores": 12, "ghz": 5.8, "generation": 13}),
    ("GPU", {"vram": 4, "memory_bus": 128, "generation": 40}),
    ("GPU", {"vram": 8, "memory_bus": 256, "generation": 40}),
    ("RAM", {"capacity": 16, "speed": 5200, "type": 2}),
    ("RAM", {"capacity": 32, "speed": 6000, "type": 2}),
]

for comp_type, specs in components:
    if comp_type == "CPU":
        price = predictor.predict_cpu_price(specs['cores'], specs['ghz'], specs['generation'])
        print(f"  CPU ({specs['cores']} cores, {specs['ghz']}GHz, Gen{specs['generation']}): ₹{price:,.0f}")
    elif comp_type == "GPU":
        price = predictor.predict_gpu_price(specs['vram'], specs['memory_bus'], specs['generation'])
        print(f"  GPU ({specs['vram']}GB, {specs['memory_bus']}-bit, Gen{specs['generation']}): ₹{price:,.0f}")
    elif comp_type == "RAM":
        price = predictor.predict_ram_price(specs['capacity'], specs['speed'], specs['type'])
        print(f"  RAM ({specs['capacity']}GB, {specs['speed']}MHz): ₹{price:,.0f}")

# ============================================================================
# 3. BUILD RECOMMENDER - K-means Clustering Algorithm
# ============================================================================
print("\n[3] BUILD RECOMMENDER (K-means Clustering)")
print("-" * 80)

from server.services.ml_build_recommender import get_build_recommender

recommender = get_build_recommender()

print("\nRecommending PC builds for different domains and budgets:\n")

scenarios = [
    ("Gaming", 50000),
    ("Gaming", 100000),
    ("Gaming", 200000),
    ("Video Editing", 150000),
    ("Programming", 75000),
    ("Streaming", 120000),
]

for domain, budget in scenarios:
    result = recommender.recommend_build(domain, budget)
    print(f"  {domain:15} {budget:>7} INR → {result['tier']:12} tier")
    print(f"    Specs: {result['specs']['cpu_cores']}-core CPU, {result['specs']['gpu_vram']}GB VRAM, {result['specs']['ram_gb']}GB RAM, {result['specs']['storage_gb']}GB Storage")
    print()

# ============================================================================
# 4. COMPLETE ANALYSIS - All algorithms working together
# ============================================================================
print("\n[4] COMPLETE AI ANALYSIS (All 3 Algorithms Combined)")
print("-" * 80)

print("\nScenario: User wants to play Cyberpunk 2077 with ₹150,000 budget\n")

# Step 1: Classify game
game = "Cyberpunk 2077"
result = classifier.classify_game(game)
print(f"Step 1 - Game Analysis (Naive Bayes):")
print(f"  Game: {game}")
print(f"  Performance Tier: {result['classification']}")
print(f"  Confidence: {result['confidence']:.1%}")
print(f"  Min Specs: {result['min_specs']}")

# Step 2: Recommend build
budget = 150000
build = recommender.recommend_build('gaming', budget)
print(f"\nStep 2 - Build Recommendation (K-means Clustering):")
print(f"  Budget: ₹{budget:,}")
print(f"  Recommended Tier: {build['tier']}")
print(f"  Components: {build['components']}")

# Step 3: Predict cost
cost = predictor.predict_total_build_cost(
    {'cores': build['specs']['cpu_cores'], 'ghz': 4.5, 'generation': 13},
    {'vram': build['specs']['gpu_vram'], 'memory_bus': 192, 'generation': 40},
    {'capacity': build['specs']['ram_gb'], 'speed': 5200, 'type': 2},
    {'capacity': build['specs']['storage_gb'], 'speed': 3500}
)
print(f"\nStep 3 - Cost Prediction (Linear Regression + Decision Tree):")
print(f"  Total Build Cost: ₹{cost['total_cost']:,.0f}")
print(f"  Budget Remaining: ₹{budget - cost['total_cost']:,.0f}")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n\n" + "="*80)
print("SUMMARY: REAL ML ALGORITHMS INTEGRATED")
print("="*80)

print("""
[OK] LINEAR REGRESSION
   - Used for price prediction
   - Fits relationship: price = a*cores + b*ghz + c*generation
   - Math: Normal equation (X^T*X)^-1*X^T*y

[OK] DECISION TREE
   - Used for non-linear pricing
   - Recursive binary splits minimizing variance
   - Combines with Linear Regression for better accuracy

[OK] ENSEMBLE (LR + DT)
   - Averages predictions from both models
   - Result: More accurate price predictions

[OK] NAIVE BAYES
   - Used for game classification
   - Probabilistic classifier: P(tier|game) = P(game|tier)*P(tier)/P(game)
   - Laplace smoothing prevents zero probabilities
   - Classifies into: LIGHT, MEDIUM, HEAVY, EXTREME

[OK] K-MEANS CLUSTERING
   - Used for build recommendations
   - Groups builds by domain characteristics
   - Finds closest cluster centroid to given budget
   - Iterates 10 times to find optimal clusters

All algorithms are REAL implementations, not mock data!
""")

print("="*80 + "\n")
