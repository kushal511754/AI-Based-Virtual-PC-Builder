"""
API routes for game and application database.
"""

from flask import Blueprint, request, jsonify
from server.services.game_database_service import GameDatabaseService

games_bp = Blueprint('games', __name__, url_prefix='/api/games')

@games_bp.route('/search', methods=['GET'])
def search_games():
    """Search games by name."""
    query = request.args.get('q', '')
    limit = request.args.get('limit', 20, type=int)
    offset = request.args.get('offset', 0, type=int)
    
    result = GameDatabaseService.get_games(query, limit, offset)
    return jsonify(result)

@games_bp.route('/popular', methods=['GET'])
def get_popular_games():
    """Get popular/trending games."""
    limit = request.args.get('limit', 12, type=int)
    
    result = GameDatabaseService.get_games(limit=limit)
    return jsonify(result)

@games_bp.route('/apps/<domain>', methods=['GET'])
def get_apps_for_domain(domain):
    """Get applications for a specific domain (video_editing, rendering, etc)."""
    search_query = request.args.get('q', None)
    limit = request.args.get('limit', 20, type=int)
    
    result = GameDatabaseService.get_apps_for_domain(domain, search_query, limit)
    return jsonify(result)

@games_bp.route('/metrics/<domain>', methods=['GET'])
def get_metrics_for_domain(domain):
    """Get performance metrics configuration for a domain."""
    metrics = GameDatabaseService.get_performance_metrics_for_domain(domain)
    
    if not metrics:
        return jsonify({
            'success': False,
            'message': f'Unknown domain: {domain}'
        }), 404
    
    return jsonify({
        'success': True,
        'domain': domain,
        'metrics': metrics
    })

