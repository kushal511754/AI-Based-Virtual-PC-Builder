"""
Game search API - ML-powered fuzzy matching for real-world games
Uses difflib and sequence matching for intelligent game name matching
"""

from flask import Blueprint, request, jsonify
import os
import csv
from pathlib import Path
from difflib import SequenceMatcher
import json

game_search_bp = Blueprint('game_ml_search', __name__, url_prefix='/api/games-search')

# Cache for games (loaded once)
GAMES_CACHE = None
CACHE_FILE = None

def get_cache_file():
    """Get path to cache file"""
    global CACHE_FILE
    if CACHE_FILE is None:
        CACHE_FILE = os.path.join(os.path.dirname(__file__), '..', '..', 'games_cache.json')
    return CACHE_FILE

def load_games_cache():
    """Load games from cache or CSV into memory"""
    global GAMES_CACHE
    
    if GAMES_CACHE is not None:
        return GAMES_CACHE
    
    cache_file = get_cache_file()
    
    # Try to load from JSON cache first
    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                GAMES_CACHE = json.load(f)
            print(f"Loaded {len(GAMES_CACHE)} games from cache")
            return GAMES_CACHE
        except:
            pass
    
    # Load from CSV
    games = []
    games_file = os.path.join(os.path.dirname(__file__), '..', '..', 'games.csv')
    
    try:
        if os.path.exists(games_file):
            print("Loading games from CSV...")
            with open(games_file, 'r', encoding='utf-8', errors='ignore') as f:
                reader = csv.DictReader(f)
                for i, row in enumerate(reader):
                    if row.get('Name') and row.get('Name').strip():
                        games.append({
                            'name': row.get('Name', '').strip(),
                            'genre': row.get('Genre', '').strip(),
                            'rating': float(row.get('Rating', 0)) if row.get('Rating') else 0,
                            'year': row.get('Year_of_Release', '').strip(),
                        })
                    
                    # Load first 50000 games for performance
                    if i >= 50000:
                        break
            
            # Save to cache
            try:
                with open(cache_file, 'w', encoding='utf-8') as f:
                    json.dump(games, f)
            except:
                pass
            
            GAMES_CACHE = games
            print(f"Loaded {len(GAMES_CACHE)} games from CSV")
        else:
            GAMES_CACHE = []
    except Exception as e:
        print(f"Error loading games: {e}")
        GAMES_CACHE = []
    
    return GAMES_CACHE

def fuzzy_match(query, game_name, threshold=0.5):
    """
    ML-based fuzzy matching using sequence similarity (SequenceMatcher DP algorithm)
    Returns match score 0-1
    """
    query_lower = query.lower().strip()
    game_lower = game_name.lower().strip()
    
    # Exact match
    if query_lower == game_lower:
        return 1.0
    
    # Contains match
    if query_lower in game_lower or game_lower in query_lower:
        return 0.95
    
    # Sequence matching (uses DP algorithm for optimal substring matching)
    ratio = SequenceMatcher(None, query_lower, game_lower).ratio()
    
    return ratio if ratio >= threshold else 0.0

def search_games_ml(query, limit=10):
    """
    Search games using ML fuzzy matching
    Returns top matches sorted by relevance score
    """
    if not query or not query.strip():
        return []
    
    games = load_games_cache()
    
    # Score all games
    scored_games = []
    for game in games:
        score = fuzzy_match(query, game['name'])
        if score > 0:
            scored_games.append({
                'name': game['name'],
                'score': score,
                'genre': game.get('genre', ''),
                'year': game.get('year', '')
            })
    
    # Sort by score (descending)
    scored_games.sort(key=lambda x: (-x['score'], x['name']))
    
    # Return top results
    return scored_games[:limit]

@game_search_bp.route('/search', methods=['GET'])
def search_games():
    """Search for games by name using ML fuzzy matching"""
    query = request.args.get('q', '').strip()
    limit = min(request.args.get('limit', 10, type=int), 50)
    
    if not query or len(query) < 1:
        return jsonify({
            'success': False,
            'games': [],
            'message': 'Query required'
        }), 400
    
    # Use ML fuzzy matching
    results = search_games_ml(query, limit)
    
    return jsonify({
        'success': True,
        'query': query,
        'games': results,
        'count': len(results)
    })

@game_search_bp.route('/autocomplete', methods=['GET'])
def autocomplete_games():
    """Autocomplete - real-time game suggestions using ML matching"""
    query = request.args.get('q', '').strip()
    limit = min(request.args.get('limit', 5, type=int), 20)
    
    if not query or len(query) < 1:
        return jsonify({
            'success': True,
            'suggestions': [],
            'count': 0
        })
    
    # Use ML fuzzy matching
    results = search_games_ml(query, limit)
    
    return jsonify({
        'success': True,
        'query': query,
        'suggestions': [r['name'] for r in results],
        'count': len(results)
    })

@game_search_bp.route('/suggest', methods=['GET'])
def suggest_games():
    """Get game suggestions based on genre or popularity"""
    domain = request.args.get('domain', 'gaming').lower()
    limit = request.args.get('limit', 5, type=int)
    
    games = load_games_cache()
    
    # Map domains to game genres
    genre_map = {
        'gaming': ['action', 'shooter', 'sports', 'rpg', 'racing'],
        'video_editing': ['simulation', 'strategy'],
        'streaming': ['action', 'shooter', 'moba', 'battle royale'],
        'rendering': ['3d', 'simulation'],
        'programming': ['puzzle', 'strategy'],
    }
    
    target_genres = genre_map.get(domain, ['action'])
    
    # Filter and sort by rating
    filtered = []
    for game in games:
        game_genre = (game.get('genre', '') or '').lower()
        for target_genre in target_genres:
            if target_genre in game_genre:
                filtered.append(game)
                break
    
    # Sort by rating (highest first)
    filtered.sort(key=lambda x: x.get('rating', 0), reverse=True)
    
    return jsonify({
        'success': True,
        'domain': domain,
        'games': filtered[:limit],
        'count': len(filtered[:limit])
    })

@game_search_bp.route('/popular', methods=['GET'])
def popular_games():
    """Get most popular/highly-rated games"""
    limit = request.args.get('limit', 20, type=int)
    
    games = load_games_cache()
    
    # Filter games with rating >= 7.0 and sort by rating
    popular = [g for g in games if g.get('rating', 0) >= 7.0]
    popular.sort(key=lambda x: x.get('rating', 0), reverse=True)
    
    return jsonify({
        'success': True,
        'games': popular[:limit],
        'count': len(popular[:limit])
    })

@game_search_bp.route('/stats', methods=['GET'])
def game_stats():
    """Get statistics about game database"""
    games = load_games_cache()
    
    total = len(games)
    genres = {}
    ratings = {'high': 0, 'medium': 0, 'low': 0}
    
    for game in games:
        genre = (game.get('genre', '') or 'Unknown').split(',')[0].strip()
        genres[genre] = genres.get(genre, 0) + 1
        
        rating = game.get('rating', 0)
        if rating >= 8:
            ratings['high'] += 1
        elif rating >= 6:
            ratings['medium'] += 1
        else:
            ratings['low'] += 1
    
    return jsonify({
        'success': True,
        'total_games': total,
        'genres': genres,
        'ratings_distribution': ratings,
        'cache_status': 'loaded' if games else 'empty'
    })
