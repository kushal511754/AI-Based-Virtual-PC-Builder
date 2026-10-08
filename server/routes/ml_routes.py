"""
ML Routes - Machine learning predictions integrated with PC builder.
Uses: Linear Regression, Decision Tree, Naive Bayes, K-means Clustering
Endpoints for price prediction, game classification, build recommendations.
"""

from flask import Blueprint, request, jsonify
import traceback

ml_bp = Blueprint('ml', __name__, url_prefix='/api/ml')

# Lazy import - only when needed
def _get_price_predictor():
    from server.services.ml_price_predictor import get_price_predictor
    return get_price_predictor()

def _get_game_classifier():
    from server.services.ml_game_classifier import get_game_classifier
    return get_game_classifier()

def _get_build_recommender():
    from server.services.ml_build_recommender import get_build_recommender
    return get_build_recommender()

# ============================================================================
# PRICE PREDICTION ENDPOINTS
# ============================================================================

@ml_bp.route('/predict-component-price', methods=['POST'])
def predict_component_price():
    """Predict component price using ML ensemble."""
    try:
        predictor = _get_price_predictor()
        data = request.get_json()
        component_type = data.get('component_type', '').lower()
        specs = data.get('specs', {})
        
        if not component_type or not specs:
            return jsonify({'success': False, 'error': 'Missing component_type or specs'}), 400
        
        if component_type == 'cpu':
            price = predictor.predict_cpu_price(specs.get('cores', 8), specs.get('ghz', 4.5), specs.get('generation', 13))
        elif component_type == 'gpu':
            price = predictor.predict_gpu_price(specs.get('vram', 6), specs.get('memory_bus', 192), specs.get('generation', 40))
        elif component_type == 'ram':
            price = predictor.predict_ram_price(specs.get('capacity', 16), specs.get('speed', 5200), specs.get('type', 2))
        elif component_type == 'storage':
            price = predictor.predict_storage_price(specs.get('capacity', 512), specs.get('speed', 3500))
        else:
            return jsonify({'success': False, 'error': f'Unknown component: {component_type}'}), 400
        
        return jsonify({'success': True, 'component_type': component_type, 'specs': specs, 'predicted_price_inr': round(price, 2), 'algorithm': 'Ensemble (Linear Regression + Decision Tree)', 'currency': 'INR'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@ml_bp.route('/predict-build-cost', methods=['POST'])
def predict_build_cost():
    """Predict total PC build cost using ML price models."""
    try:
        predictor = _get_price_predictor()
        data = request.get_json()
        result = predictor.predict_total_build_cost(data.get('cpu_specs', {}), data.get('gpu_specs', {}), data.get('ram_specs', {}), data.get('storage_specs', {}))
        return jsonify({'success': True, **result, 'message': 'Total build cost predicted using ML ensemble models'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================================================
# GAME CLASSIFICATION ENDPOINTS (Naive Bayes)
# ============================================================================

@ml_bp.route('/classify-game-requirements', methods=['POST'])
def classify_game_requirements():
    """Classify game by performance requirements using Naive Bayes algorithm."""
    try:
        classifier = _get_game_classifier()
        data = request.get_json()
        game_name = data.get('game_name', '')
        
        if not game_name:
            return jsonify({'success': False, 'error': 'Missing game_name'}), 400
        
        result = classifier.classify_game(game_name, game_type=data.get('game_type'), year=data.get('release_year'), is_aaa=data.get('is_aaa'))
        return jsonify({'success': True, **result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================================================
# BUILD RECOMMENDATION ENDPOINTS (K-means Clustering)
# ============================================================================

@ml_bp.route('/recommend-build', methods=['POST'])
def recommend_build():
    """Recommend PC build using K-means clustering algorithm."""
    try:
        recommender = _get_build_recommender()
        data = request.get_json()
        domain = data.get('domain', 'gaming').lower()
        budget = data.get('budget_inr', 75000)
        game_reqs = data.get('game_requirements')
        
        result = recommender.recommend_build(domain, budget, game_reqs)
        return jsonify({'success': True, **result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================================================
# COMBINED ANALYSIS ENDPOINT
# ============================================================================

@ml_bp.route('/get-ai-optimized-build', methods=['POST'])
def get_ai_optimized_build():
    """Combined ML analysis: Classify game + Recommend build + Predict cost."""
    try:
        classifier = _get_game_classifier()
        recommender = _get_build_recommender()
        predictor = _get_price_predictor()
        
        data = request.get_json()
        game_name = data.get('game_name', 'Unknown Game')
        domain = data.get('domain', 'gaming')
        budget_inr = data.get('budget_inr', 75000)
        
        # Step 1: Classify game (Naive Bayes)
        game_analysis = classifier.classify_game(game_name)
        
        # Step 2: Recommend build (K-means)
        game_reqs = {'cpu_cores': game_analysis['min_specs']['cpu_cores'], 'gpu_vram': game_analysis['min_specs']['gpu_vram'], 'ram_gb': game_analysis['min_specs']['ram_gb']}
        build_rec = recommender.recommend_build(domain, budget_inr, game_reqs)
        
        # Step 3: Predict cost (Ensemble)
        cost_pred = predictor.predict_total_build_cost(
            {'cores': build_rec['specs']['cpu_cores'], 'ghz': 4.5, 'generation': 13},
            {'vram': build_rec['specs']['gpu_vram'], 'memory_bus': 192, 'generation': 40},
            {'capacity': build_rec['specs']['ram_gb'], 'speed': 5200, 'type': 2},
            {'capacity': build_rec['specs']['storage_gb'], 'speed': 3500}
        )
        
        return jsonify({
            'success': True,
            'game_name': game_name,
            'game_analysis': {'classification': game_analysis['classification'], 'confidence': game_analysis['confidence'], 'min_specs': game_analysis['min_specs'], 'recommended_specs': game_analysis['recommended_specs'], 'predicted_fps': game_analysis['predicted_fps']},
            'build_recommendation': {'tier': build_rec['tier'], 'domain': build_rec['domain'], 'specs': build_rec['specs'], 'components': build_rec['components'], 'budget_utilization': build_rec['budget_utilization']},
            'cost_prediction': cost_pred,
            'algorithms': ['Naive Bayes Classification', 'K-means Clustering', 'Ensemble (Linear Regression + Decision Tree)']
        })
    except Exception as e:
        error_msg = 'Combined analysis error'
        return jsonify({'success': False, 'error': error_msg}), 500

# ============================================================================
# HEALTH CHECK ENDPOINT
# ============================================================================

@ml_bp.route('/health', methods=['GET'])
def ml_health():
    """Check if ML services are loaded and working."""
    try:
        predictor = _get_price_predictor()
        classifier = _get_game_classifier()
        recommender = _get_build_recommender()
        
        return jsonify({
            'success': True,
            'status': 'Ready',
            'ml_services': {'price_predictor': 'Ready', 'game_classifier': 'Ready', 'build_recommender': 'Ready'},
            'algorithms': ['Linear Regression', 'Decision Tree', 'Naive Bayes Classification', 'K-means Clustering'],
            'endpoints': ['/api/ml/predict-component-price', '/api/ml/predict-build-cost', '/api/ml/classify-game-requirements', '/api/ml/recommend-build', '/api/ml/get-ai-optimized-build', '/api/ml/health']
        })
    except Exception as e:
        error_msg = 'ML service error'
        return jsonify({'success': False, 'error': error_msg, 'message': 'Error checking ML services'}), 500
