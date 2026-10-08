"""
ML Game Classifier - Classifies games by performance requirements using Naive Bayes algorithm.
Fast classification without API calls.
"""

import math
from collections import defaultdict

class MLGameClassifier:
    """
    Game Classifier using Naive Bayes algorithm.
    Classifies games into: LIGHT, MEDIUM, HEAVY, EXTREME
    
    Based on game characteristics:
    - Release year (newer = heavier usually)
    - Game type (FPS, RPG, Strategy, etc.)
    - Known requirements
    """
    
    def __init__(self):
        """Initialize Naive Bayes classifier with training data."""
        self.class_priors = {}
        self.feature_likelihoods = defaultdict(lambda: defaultdict(float))
        self.classes = ['LIGHT', 'MEDIUM', 'HEAVY', 'EXTREME']
        self.train_classifier()
    
    def train_classifier(self):
        """Train Naive Bayes classifier with game data."""
        # Training data: (game_type, year, is_aaa, class)
        training_data = [
            # LIGHT games
            ('2D Platformer', 2020, False, 'LIGHT'),
            ('Puzzle', 2022, False, 'LIGHT'),
            ('Indie Platformer', 2021, False, 'LIGHT'),
            ('Point-and-Click', 2019, False, 'LIGHT'),
            ('Turn-based Strategy', 2023, False, 'LIGHT'),
            ('Valorant', 2020, True, 'LIGHT'),
            ('BGMI', 2021, False, 'LIGHT'),
            ('Dota 2', 2013, True, 'LIGHT'),
            
            # MEDIUM games
            ('Action Game', 2022, True, 'MEDIUM'),
            ('Third-Person Shooter', 2021, True, 'MEDIUM'),
            ('RPG', 2023, True, 'MEDIUM'),
            ('Racing Game', 2022, True, 'MEDIUM'),
            ('Fighting Game', 2023, True, 'MEDIUM'),
            ('Sports Game', 2023, True, 'MEDIUM'),
            ('Fortnite', 2017, True, 'MEDIUM'),
            ('Overwatch 2', 2022, True, 'MEDIUM'),
            
            # HEAVY games
            ('AAA RPG', 2023, True, 'HEAVY'),
            ('Open World', 2022, True, 'HEAVY'),
            ('Witcher 3', 2015, True, 'HEAVY'),
            ('GTA V', 2013, True, 'HEAVY'),
            ('Cyberpunk 2077', 2020, True, 'HEAVY'),
            ('Elden Ring', 2022, True, 'HEAVY'),
            ('Metro Exodus', 2019, True, 'HEAVY'),
            ('Red Dead Redemption 2', 2018, True, 'HEAVY'),
            
            # EXTREME games
            ('Helldivers 2', 2024, True, 'EXTREME'),
            ('Starfield', 2023, True, 'EXTREME'),
            ('Baldur\'s Gate 3', 2023, True, 'EXTREME'),
            ('Avatar Frontiers', 2023, True, 'EXTREME'),
            ('Alan Wake 2', 2023, True, 'EXTREME'),
            ('Indiana Jones Game', 2024, True, 'EXTREME'),
        ]
        
        # Count class occurrences
        class_counts = defaultdict(int)
        total = len(training_data)
        
        for game_type, year, is_aaa, game_class in training_data:
            class_counts[game_class] += 1
        
        # Calculate class priors: P(Class)
        for game_class in self.classes:
            self.class_priors[game_class] = math.log(max(class_counts[game_class], 1) / total)
        
        # Calculate feature likelihoods for each class
        feature_class_counts = defaultdict(lambda: defaultdict(int))
        
        for game_type, year, is_aaa, game_class in training_data:
            # Features: game_type, year_range, aaa_status
            year_range = self._get_year_range(year)
            aaa_str = 'AAA' if is_aaa else 'Indie'
            
            feature_class_counts[('type', game_type)][game_class] += 1
            feature_class_counts[('year', year_range)][game_class] += 1
            feature_class_counts[('aaa', aaa_str)][game_class] += 1
        
        # Calculate P(Feature | Class) with Laplace smoothing
        for feature, class_dict in feature_class_counts.items():
            for game_class in self.classes:
                count = class_dict.get(game_class, 0)
                # Laplace smoothing: (count + 1) / (total_in_class + feature_values)
                total_in_class = class_counts[game_class]
                self.feature_likelihoods[feature][game_class] = math.log(max(count + 1, 1) / (total_in_class + 2))
    
    def _get_year_range(self, year):
        """Convert year to range for feature."""
        if year < 2015:
            return 'Old'
        elif year < 2020:
            return 'Recent'
        else:
            return 'New'
    
    def classify_game(self, game_name, game_type=None, year=None, is_aaa=None):
        """
        Classify a game into performance requirement class.
        
        Args:
            game_name: Name of the game
            game_type: Type of game (optional)
            year: Release year (optional, defaults to 2024)
            is_aaa: Is AAA game (optional, inferred from type)
        
        Returns:
            {
                'game_name': str,
                'classification': 'LIGHT'|'MEDIUM'|'HEAVY'|'EXTREME',
                'confidence': float (0-1),
                'min_specs': dict,
                'recommended_specs': dict,
                'predicted_fps': dict
            }
        """
        # Infer missing features
        if year is None:
            year = 2024
        
        if game_type is None:
            game_type = self._infer_game_type(game_name)
        
        if is_aaa is None:
            is_aaa = self._infer_aaa_status(game_name, game_type)
        
        # Apply Naive Bayes classification
        scores = {}
        for game_class in self.classes:
            # P(Class | Features) ∝ P(Class) * P(Feature1|Class) * P(Feature2|Class) * ...
            score = self.class_priors[game_class]
            
            year_range = self._get_year_range(year)
            aaa_str = 'AAA' if is_aaa else 'Indie'
            
            # Add feature contributions
            score += self.feature_likelihoods[('type', game_type)][game_class]
            score += self.feature_likelihoods[('year', year_range)][game_class]
            score += self.feature_likelihoods[('aaa', aaa_str)][game_class]
            
            scores[game_class] = score
        
        # Get classification with highest probability
        best_class = max(scores, key=scores.get)
        
        # Calculate confidence (softmax)
        exp_scores = {k: math.exp(v) for k, v in scores.items()}
        total = sum(exp_scores.values())
        confidence = exp_scores[best_class] / total
        
        # Generate specs based on classification
        specs = self._get_specs_for_class(best_class)
        fps = self._get_fps_for_class(best_class)
        
        return {
            'game_name': game_name,
            'classification': best_class,
            'confidence': round(confidence, 3),
            'game_type': game_type,
            'release_year': year,
            'is_aaa': is_aaa,
            'min_specs': specs['minimum'],
            'recommended_specs': specs['recommended'],
            'predicted_fps': fps,
            'algorithm': 'Naive Bayes Classifier'
        }
    
    def _infer_game_type(self, game_name):
        """Infer game type from name using keyword matching."""
        name_lower = game_name.lower()
        
        keywords = {
            'RPG': ['rpg', 'role-playing', 'witcher', 'elden ring', 'baldur', 'elder'],
            'FPS': ['fps', 'call of duty', 'counter-strike', 'valorant', 'halo', 'overwatch'],
            'Racing': ['racing', 'forza', 'gran turismo', 'f1'],
            'Action': ['action', 'cyberpunk', 'assassin', 'kingdom come'],
            'Strategy': ['strategy', 'starcraft', 'civilization', 'total war'],
            'Sports': ['sports', 'fifa', 'madden', 'nba', 'nfl'],
            'Indie': ['indie', 'hollow knight', 'stardew'],
        }
        
        for game_type, keys in keywords.items():
            for key in keys:
                if key in name_lower:
                    return game_type
        
        return 'Action Game'  # Default
    
    def _infer_aaa_status(self, game_name, game_type):
        """Infer if game is AAA from name and type."""
        aaa_games = [
            'cyberpunk', 'witcher', 'elden ring', 'baldur\'s gate',
            'starfield', 'gta', 'red dead', 'cyberpunk', 'hogwarts',
            'call of duty', 'battlefield', 'fortnite', 'overwatch',
            'assassin\'s creed', 'kingdom come', 'metro', 'helldivers'
        ]
        
        name_lower = game_name.lower()
        for aaa_game in aaa_games:
            if aaa_game in name_lower:
                return True
        
        # Games with "AAA" or from major studios are AAA
        return False
    
    def _get_specs_for_class(self, classification):
        """Get hardware specs based on classification."""
        specs_dict = {
            'LIGHT': {
                'minimum': {
                    'cpu_cores': 2,
                    'gpu_vram': 1,
                    'ram_gb': 4,
                    'storage_gb': 20,
                    'examples': 'BGMI, Valorant, 2D Games'
                },
                'recommended': {
                    'cpu_cores': 4,
                    'gpu_vram': 2,
                    'ram_gb': 8,
                    'storage_gb': 50,
                    'examples': 'Smooth 1080p 60fps'
                }
            },
            'MEDIUM': {
                'minimum': {
                    'cpu_cores': 4,
                    'gpu_vram': 3,
                    'ram_gb': 8,
                    'storage_gb': 80,
                    'examples': 'Fortnite, Overwatch 2'
                },
                'recommended': {
                    'cpu_cores': 6,
                    'gpu_vram': 6,
                    'ram_gb': 16,
                    'storage_gb': 100,
                    'examples': '1080p High 100fps'
                }
            },
            'HEAVY': {
                'minimum': {
                    'cpu_cores': 6,
                    'gpu_vram': 4,
                    'ram_gb': 12,
                    'storage_gb': 120,
                    'examples': 'Witcher 3, GTA V'
                },
                'recommended': {
                    'cpu_cores': 8,
                    'gpu_vram': 8,
                    'ram_gb': 16,
                    'storage_gb': 150,
                    'examples': '1440p Ultra 60fps'
                }
            },
            'EXTREME': {
                'minimum': {
                    'cpu_cores': 8,
                    'gpu_vram': 6,
                    'ram_gb': 16,
                    'storage_gb': 150,
                    'examples': 'Cyberpunk 2077, Starfield'
                },
                'recommended': {
                    'cpu_cores': 12,
                    'gpu_vram': 12,
                    'ram_gb': 32,
                    'storage_gb': 200,
                    'examples': '1440p Ultra 100fps or 4K 60fps'
                }
            }
        }
        
        return specs_dict.get(classification, specs_dict['MEDIUM'])
    
    def _get_fps_for_class(self, classification):
        """Get predicted FPS ranges based on classification."""
        fps_dict = {
            'LIGHT': {
                '1080p_low': '120+ FPS',
                '1080p_high': '100+ FPS',
                '1440p_high': '80+ FPS',
                '4k_high': '60+ FPS'
            },
            'MEDIUM': {
                '1080p_low': '150+ FPS',
                '1080p_high': '100-120 FPS',
                '1440p_high': '60-80 FPS',
                '4k_high': '40-60 FPS'
            },
            'HEAVY': {
                '1080p_low': '100+ FPS',
                '1080p_high': '60-90 FPS',
                '1440p_high': '40-60 FPS',
                '4k_high': '20-30 FPS'
            },
            'EXTREME': {
                '1080p_low': '80-100 FPS',
                '1080p_high': '50-70 FPS',
                '1440p_high': '30-50 FPS',
                '4k_high': '15-25 FPS'
            }
        }
        
        return fps_dict.get(classification, fps_dict['MEDIUM'])

# Global instance
_classifier = None

def get_game_classifier():
    """Get or create global game classifier instance."""
    global _classifier
    if _classifier is None:
        _classifier = MLGameClassifier()
    return _classifier
