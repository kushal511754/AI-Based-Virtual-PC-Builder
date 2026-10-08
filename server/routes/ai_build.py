"""
API routes for AI-powered PC build recommendations.
"""

from flask import Blueprint, request, jsonify
import os
from dotenv import load_dotenv

load_dotenv()

ai_bp = Blueprint('ai', __name__, url_prefix='/api/ai')

# Lazy imports - only load when endpoint is called
def _get_ai_service():
    from server.services.ai_build_service import AIBuildService
    return AIBuildService

def _get_game_analyzer():
    from server.services.openai_game_analyzer import OpenAIGameAnalyzer
    return OpenAIGameAnalyzer

@ai_bp.route('/domains', methods=['GET'])
def get_domains():
    """Get all available domains for AI build."""
    AIBuildService = _get_ai_service()
    domains = AIBuildService.get_domains()
    return jsonify({
        'success': True,
        'domains': [
            {
                'id': key,
                'name': value['name'],
                'min_cpu_cores': value['min_cpu_cores'],
                'min_gpu_vram': value['min_gpu_vram'],
                'min_ram_gb': value['min_ram_gb'],
                'min_storage_gb': value['min_storage_gb'],
                'priority': value['priority'],
                'description': f"For {value['name'].lower()} tasks"
            }
            for key, value in domains.items()
        ]
    })

def _normalize_domain(d):
    if not d:
        return 'gaming'
    d_clean = str(d).lower().strip()
    mapping = {
        'gaming': 'gaming',
        'video editing': 'video_editing',
        'video_editing': 'video_editing',
        'development': 'programming',
        'programming': 'programming',
        'software': 'programming',
        'streaming': 'streaming',
        'rendering': 'rendering',
        '3d rendering': 'rendering',
        '3d_rendering': 'rendering',
        'ai / machine learning': 'rendering',
        'ai_machine_learning': 'rendering',
        'productivity': 'general_purpose',
        'general': 'general_purpose',
        'general_purpose': 'general_purpose'
    }
    return mapping.get(d_clean, 'gaming')

@ai_bp.route('/check-budget', methods=['POST'])
def check_budget():
    """Check if budget is sufficient for domain."""
    AIBuildService = _get_ai_service()
    data = request.get_json() or {}
    domain = _normalize_domain(data.get('domain'))
    budget = data.get('budget', 0)
    
    if not domain or budget <= 0:
        return jsonify({'success': False, 'message': 'Invalid domain or budget'}), 400
    
    result = AIBuildService.analyze_budget(domain, budget)
    return jsonify({
        'success': result['sufficient'],
        'sufficient': result['sufficient'],
        'message': result['message'],
        'budget_breakdown': result['budget_breakdown'],
        'budget_deficit': result.get('budget_deficit', 0)
    })

@ai_bp.route('/suggest-build', methods=['POST'])
def suggest_build():
    """Get AI-suggested PC build for domain, game, and budget."""
    AIBuildService = _get_ai_service()
    data = request.get_json() or {}
    domain = _normalize_domain(data.get('domain'))
    game_name = data.get('game_name', 'Cyberpunk 2077')
    budget = data.get('budget', 0)
    
    if not domain or budget <= 0:
        return jsonify({'success': False, 'message': 'Invalid domain or budget'}), 400
    
    result = AIBuildService.get_ai_suggestion(domain, game_name, budget)
    
    if result['success']:
        # Convert all parts to plain dicts for JSON serialization
        suggested_parts = {}
        for key in ['cpu', 'gpu', 'motherboard', 'ram', 'storage', 'psu', 'case', 'cooling']:
            part = result['suggested_parts'].get(key)
            if part:
                # Convert sqlite3.Row to plain dict
                suggested_parts[key] = dict(part) if hasattr(part, 'keys') else part
            else:
                suggested_parts[key] = None
        
        return jsonify({
            'success': True,
            'message': result['message'],
            'domain': result['domain'],
            'game_name': result['game_name'],
            'budget': result['budget'],
            'total_price': result['total_price'],
            'budget_check': result['budget_check'],
            'suggested_parts': suggested_parts,
            'compatibility': result['compatibility'],
            'currency': result.get('currency', 'INR'),
            'price_source': result.get('price_source', 'Indian Market (PCBuild Agent)'),
            'validation_logs': result.get('validation_logs', [])
        })
    else:
        return jsonify({
            'success': False,
            'message': result['message'],
            'budget_check': result['budget_check']
        }), 400

@ai_bp.route('/game-requirements', methods=['GET', 'POST'])
def get_game_requirements():
    """
    Get hardware requirements for any game using OpenAI GPT.
    Supports any game: BGMI, Cyberpunk 2077, PUBG Mobile, etc.
    First searches 506-game database, then falls back to OpenAI.
    """
    try:
        if request.method == 'POST':
            data = request.get_json()
            game_name = data.get('game_name', '').strip()
        else:
            game_name = request.args.get('game_name', '').strip()
        
        if not game_name or len(game_name) < 2:
            return jsonify({'success': False, 'error': 'Please provide a valid game name'}), 400
        
        OpenAIGameAnalyzer = _get_game_analyzer()
        analyzer = OpenAIGameAnalyzer()
        result = analyzer.extract_game_requirements(game_name)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error fetching game requirements: {str(e)}'
        }), 500

@ai_bp.route('/game-build-recommendation', methods=['POST'])
def get_game_build_recommendation():
    """
    Get complete PC build recommendation for a game and budget using OpenAI.
    """
    try:
        data = request.get_json()
        game_name = data.get('game_name', '').strip()
        budget_inr = data.get('budget', 0)
        domain = data.get('domain', 'gaming')
        
        if not game_name or len(game_name) < 2:
            return jsonify({'success': False, 'error': 'Please provide a valid game name'}), 400
        
        if budget_inr <= 0:
            return jsonify({'success': False, 'error': 'Please provide a valid budget'}), 400
        
        # Check if OpenAI API key is configured
        if not os.getenv('OPENAI_API_KEY'):
            return jsonify({
                'success': False,
                'error': 'OpenAI API key not configured.'
            }), 500
        
        OpenAIGameAnalyzer = _get_game_analyzer()
        analyzer = OpenAIGameAnalyzer()
        result = analyzer.get_game_and_build_recommendation(game_name, budget_inr)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error generating recommendation: {str(e)}'
        }), 500

@ai_bp.route('/validate-pc-for-game', methods=['POST'])
def validate_pc_for_game_route():
    """
    Validate if a PC build can run a specific game.
    """
    try:
        data = request.get_json()
        game_name = data.get('game_name', '').strip()
        pc_specs = data.get('pc_specs', {})
        
        if not game_name or len(game_name) < 2:
            return jsonify({'success': False, 'error': 'Please provide a valid game name'}), 400
        
        if not pc_specs:
            return jsonify({'success': False, 'error': 'Please provide PC specifications'}), 400
        
        # Check if OpenAI API key is configured
        if not os.getenv('OPENAI_API_KEY'):
            return jsonify({
                'success': False,
                'error': 'OpenAI API key not configured.'
            }), 500
        
        OpenAIGameAnalyzer = _get_game_analyzer()
        analyzer = OpenAIGameAnalyzer()
        result = analyzer.validate_pc_for_game(game_name, pc_specs)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error validating PC: {str(e)}'
        }), 500

@ai_bp.route('/search-games', methods=['GET', 'POST'])
def search_games_db():
    """
    Search games in the 506-game database (6 core + 500 Steam).
    Returns matching games with their specs.
    """
    try:
        if request.method == 'POST':
            data = request.get_json()
            query = data.get('query', '').strip()
        else:
            query = request.args.get('query', '').strip()
        
        if not query or len(query) < 1:
            return jsonify({'success': False, 'error': 'Please provide a search query'}), 400
        
        OpenAIGameAnalyzer = _get_game_analyzer()
        analyzer = OpenAIGameAnalyzer()
        games = analyzer.search_games(query)
        
        return jsonify({
            'success': True,
            'query': query,
            'total_found': len(games),
            'games': games
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error searching games: {str(e)}'
        }), 500
