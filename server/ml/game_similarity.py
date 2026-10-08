"""
ML Model: Game Similarity & Semantic Search
Uses embeddings to find similar games and semantic search.
Falls back to basic string matching if transformers unavailable.
"""

import os
import json
import numpy as np
import pickle

try:
    from sentence_transformers import SentenceTransformer
    HAS_TRANSFORMERS = True
except ImportError:
    HAS_TRANSFORMERS = False

class GameSimilarityEngine:
    """
    Find similar games using semantic embeddings.
    Supports: "Find games like BGMI", "Games similar to Cyberpunk"
    """
    
    # Predefined game embeddings (fallback data)
    GAME_DATABASE = {
        'BGMI': {
            'full_name': 'Battlegrounds Mobile India',
            'category': 'Battle Royale',
            'platform': 'Mobile',
            'keywords': ['battle royale', 'fps', 'mobile', 'tactical', 'competitive']
        },
        'Cyberpunk 2077': {
            'full_name': 'Cyberpunk 2077',
            'category': 'Action RPG',
            'platform': 'PC/Console',
            'keywords': ['action', 'rpg', 'open world', 'sci-fi', 'narrative']
        },
        'Fortnite': {
            'full_name': 'Fortnite Battle Royale',
            'category': 'Battle Royale',
            'platform': 'Multi-platform',
            'keywords': ['battle royale', 'shooter', 'multiplayer', 'colorful']
        },
        'Valorant': {
            'full_name': 'Valorant',
            'category': 'Tactical FPS',
            'platform': 'PC',
            'keywords': ['tactical', 'fps', 'competitive', 'esports', 'round-based']
        },
        'GTA V': {
            'full_name': 'Grand Theft Auto V',
            'category': 'Action Adventure',
            'platform': 'PC/Console',
            'keywords': ['open world', 'action', 'crime', 'story-driven']
        },
        'Elden Ring': {
            'full_name': 'Elden Ring',
            'category': 'Action RPG',
            'platform': 'PC/Console',
            'keywords': ['rpg', 'action', 'souls-like', 'fantasy', 'challenging']
        },
        'Minecraft': {
            'full_name': 'Minecraft',
            'category': 'Sandbox',
            'platform': 'Multi-platform',
            'keywords': ['sandbox', 'creative', 'exploration', 'building', 'procedural']
        },
        'The Witcher 3': {
            'full_name': 'The Witcher 3: Wild Hunt',
            'category': 'Action RPG',
            'platform': 'PC/Console',
            'keywords': ['rpg', 'action', 'open world', 'story', 'fantasy']
        },
        'Helldivers 2': {
            'full_name': 'Helldivers 2',
            'category': 'Third-Person Shooter',
            'platform': 'PC/Console',
            'keywords': ['shooter', 'cooperative', 'tactical', 'alien', 'squad']
        },
        'Starfield': {
            'full_name': 'Starfield',
            'category': 'Space RPG',
            'platform': 'PC/Console',
            'keywords': ['space', 'rpg', 'exploration', 'science fiction', 'open world']
        }
    }
    
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        """Initialize similarity engine with embeddings model."""
        self.model_name = model_name
        self.model = None
        self.embeddings_cache = {}
        self.has_embeddings = False
        
        if HAS_TRANSFORMERS:
            try:
                print("🔧 Loading semantic embeddings model...")
                self.model = SentenceTransformer(model_name)
                self.has_embeddings = True
                print("✅ Embeddings model loaded!")
                self._precompute_embeddings()
            except Exception as e:
                print(f"⚠️ Could not load embeddings: {e}")
                self.has_embeddings = False
        else:
            print("⚠️ sentence-transformers not installed. Using fallback mode.")
    
    def _precompute_embeddings(self):
        """Precompute embeddings for all known games."""
        if not self.has_embeddings:
            return
        
        try:
            for game_name in self.GAME_DATABASE.keys():
                keywords = self.GAME_DATABASE[game_name]['keywords']
                text = f"{game_name} {' '.join(keywords)}"
                self.embeddings_cache[game_name] = self.model.encode(text)
        except Exception as e:
            print(f"Warning: Could not precompute embeddings: {e}")
    
    def find_similar_games(self, game_name: str, top_k: int = 5) -> list:
        """
        Find games similar to the given game.
        
        Args:
            game_name: Name of the game
            top_k: Number of similar games to return
        
        Returns:
            List of similar games with similarity scores
        """
        if not game_name:
            return []
        
        # Normalize game name
        game_name_normalized = game_name.strip().lower()
        
        # Find exact match in database
        exact_match = None
        for db_game in self.GAME_DATABASE.keys():
            if db_game.lower() == game_name_normalized:
                exact_match = db_game
                break
        
        if not exact_match:
            # Try substring match
            for db_game in self.GAME_DATABASE.keys():
                if game_name_normalized in db_game.lower():
                    exact_match = db_game
                    break
        
        if not exact_match:
            return self._fallback_similar_search(game_name)
        
        if self.has_embeddings and exact_match in self.embeddings_cache:
            return self._embedding_based_search(exact_match, top_k)
        else:
            return self._category_based_search(exact_match, top_k)
    
    def _embedding_based_search(self, game_name: str, top_k: int) -> list:
        """Find similar games using embeddings."""
        try:
            query_embedding = self.embeddings_cache[game_name]
            
            similarities = []
            for other_game, other_embedding in self.embeddings_cache.items():
                if other_game != game_name:
                    # Cosine similarity
                    similarity = np.dot(query_embedding, other_embedding) / (
                        np.linalg.norm(query_embedding) * np.linalg.norm(other_embedding)
                    )
                    similarities.append((other_game, similarity))
            
            # Sort by similarity
            similarities.sort(key=lambda x: x[1], reverse=True)
            
            return [
                {
                    'game': game,
                    'similarity': round(score, 3),
                    'category': self.GAME_DATABASE[game]['category'],
                    'reason': 'Semantic similarity'
                }
                for game, score in similarities[:top_k]
            ]
        
        except Exception as e:
            print(f"Error in embedding search: {e}")
            return []
    
    def _category_based_search(self, game_name: str, top_k: int) -> list:
        """Find similar games by category (fallback)."""
        game_info = self.GAME_DATABASE[game_name]
        game_category = game_info['category']
        game_keywords = set(game_info['keywords'])
        
        similarities = []
        
        for other_game, other_info in self.GAME_DATABASE.items():
            if other_game != game_name:
                other_category = other_info['category']
                other_keywords = set(other_info['keywords'])
                
                # Category match (0.7 weight)
                category_score = 0.7 if other_category == game_category else 0.3
                
                # Keyword overlap (0.3 weight)
                if other_keywords and game_keywords:
                    keyword_score = len(game_keywords & other_keywords) / len(game_keywords | other_keywords)
                else:
                    keyword_score = 0
                
                total_score = (category_score * 0.7) + (keyword_score * 0.3)
                similarities.append((other_game, total_score))
        
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        return [
            {
                'game': game,
                'similarity': round(score, 3),
                'category': self.GAME_DATABASE[game]['category'],
                'reason': f'Similar to {game_category}'
            }
            for game, score in similarities[:top_k]
        ]
    
    def _fallback_similar_search(self, game_name: str) -> list:
        """Fallback when game not in database."""
        return [
            {
                'game': game,
                'similarity': 0.5,
                'category': self.GAME_DATABASE[game]['category'],
                'reason': 'Popular alternative'
            }
            for game in list(self.GAME_DATABASE.keys())[:5]
        ]
    
    def semantic_search(self, query: str) -> dict:
        """
        Search for games using natural language.
        Examples: "Games like BGMI", "Tactical shooters", "Open world RPGs"
        
        Args:
            query: Natural language search query
        
        Returns:
            {
                'results': [list of games],
                'query': str,
                'method': str
            }
        """
        query_lower = query.lower()
        
        # Extract game name if mentioned
        for game in self.GAME_DATABASE.keys():
            if game.lower() in query_lower:
                return {
                    'results': self.find_similar_games(game, top_k=5),
                    'query': query,
                    'method': 'Game-based similarity'
                }
        
        # Category-based search
        if 'tactical' in query_lower or 'tactical fps' in query_lower:
            return {
                'results': [
                    {'game': 'Valorant', 'match': 'Tactical FPS'},
                    {'game': 'BGMI', 'match': 'Tactical shooter'}
                ],
                'query': query,
                'method': 'Category search'
            }
        
        if 'rpg' in query_lower or 'open world' in query_lower:
            return {
                'results': [
                    {'game': 'Cyberpunk 2077', 'match': 'Action RPG'},
                    {'game': 'GTA V', 'match': 'Open world'},
                    {'game': 'The Witcher 3', 'match': 'Open world RPG'}
                ],
                'query': query,
                'method': 'Category search'
            }
        
        # Default: return all games
        return {
            'results': [
                {'game': g, 'category': self.GAME_DATABASE[g]['category']}
                for g in self.GAME_DATABASE.keys()
            ],
            'query': query,
            'method': 'Keyword fallback'
        }

# Global instance
_similarity_engine = None

def get_similarity_engine():
    """Get or create similarity engine."""
    global _similarity_engine
    if _similarity_engine is None:
        _similarity_engine = GameSimilarityEngine()
    return _similarity_engine
