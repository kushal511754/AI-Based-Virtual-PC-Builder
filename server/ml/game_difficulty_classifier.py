"""
ML Model: Game Difficulty Classifier
Classifies games as Light/Medium/Heavy based on hardware requirements.
Uses: Gradient Boosting Classifier with game specifications
"""

import os
import numpy as np
import joblib
from datetime import datetime

try:
    from sklearn.ensemble import GradientBoostingClassifier
    from sklearn.preprocessing import StandardScaler, LabelEncoder
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score, classification_report
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False

class GameDifficultyClassifier:
    """
    Classifies game hardware requirements difficulty level.
    Classes: 'Light' (easy to run), 'Medium' (moderate), 'Heavy' (demanding)
    """
    
    # Training data: (game_name, min_ram_gb, min_vram_gb, min_cpu_cores, difficulty)
    TRAINING_DATA = [
        # Light games (easy to run)
        ('Minecraft', 2, 1, 2, 'Light'),
        ('Valorant', 4, 1, 2, 'Light'),
        ('CS:GO', 4, 2, 2, 'Light'),
        ('Dota 2', 4, 2, 2, 'Light'),
        ('League of Legends', 4, 1, 2, 'Light'),
        ('Fortnite (Low)', 4, 2, 2, 'Light'),
        ('BGMI (Mobile)', 3, 1, 2, 'Light'),
        ('Roblox', 2, 1, 2, 'Light'),
        
        # Medium games (moderate requirements)
        ('GTA V', 8, 3, 4, 'Medium'),
        ('Fortnite (High)', 8, 4, 4, 'Medium'),
        ('Valorant (Ultra)', 8, 4, 4, 'Medium'),
        ('Rust', 8, 4, 4, 'Medium'),
        ('Escape from Tarkov', 12, 4, 4, 'Medium'),
        ('Call of Duty Modern Warfare', 8, 4, 4, 'Medium'),
        ('Warzone', 8, 4, 4, 'Medium'),
        ('The Witcher 3 (High)', 8, 6, 6, 'Medium'),
        ('Apex Legends', 8, 4, 4, 'Medium'),
        ('Valorant 4K', 8, 6, 6, 'Medium'),
        
        # Heavy games (demanding)
        ('Cyberpunk 2077 (Ultra)', 16, 8, 8, 'Heavy'),
        ('The Witcher 3 (Ultra)', 12, 8, 8, 'Heavy'),
        ('Elden Ring (Ultra)', 12, 8, 8, 'Heavy'),
        ('Red Dead Redemption 2', 16, 8, 8, 'Heavy'),
        ('Microsoft Flight Simulator', 16, 8, 6, 'Heavy'),
        ('Star Citizen', 32, 8, 8, 'Heavy'),
        ('Starfield (Ultra)', 16, 12, 12, 'Heavy'),
        ('Avatar Frontiers of Pandora', 24, 12, 12, 'Heavy'),
        ('Unreal Engine 5 Demos', 32, 16, 16, 'Heavy'),
        ('3DMark Ultra', 16, 12, 12, 'Heavy'),
        ('Blender (Professional)', 64, 8, 16, 'Heavy'),
        ('Adobe Premier Pro 4K', 32, 6, 12, 'Heavy'),
        ('Helldivers 2 (4K)', 16, 8, 8, 'Heavy'),
    ]
    
    def __init__(self, model_path='server/ml/models/game_classifier.pkl'):
        """Initialize game difficulty classifier."""
        self.model_path = model_path
        self.scaler = None
        self.model = None
        self.label_encoder = None
        self.is_trained = False
        
        if not HAS_SKLEARN:
            print("⚠️ scikit-learn not installed. Difficulty classification will use fallback mode.")
            return
        
        # Try to load pre-trained model
        if os.path.exists(model_path):
            self._load_model()
        else:
            self._train_model()
    
    def _train_model(self):
        """Train Gradient Boosting model on game data."""
        if not HAS_SKLEARN:
            return
        
        try:
            print("🔧 Training Game Difficulty Classifier...")
            
            # Prepare training data
            X_list = []
            y_list = []
            
            for game, min_ram, min_vram, min_cores, difficulty in self.TRAINING_DATA:
                X_list.append([min_ram, min_vram, min_cores])
                y_list.append(difficulty)
            
            X = np.array(X_list)
            y = np.array(y_list)
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y
            )
            
            # Scale features
            self.scaler = StandardScaler()
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            # Train Gradient Boosting Classifier
            self.model = GradientBoostingClassifier(
                n_estimators=100,
                max_depth=5,
                learning_rate=0.1,
                random_state=42
            )
            
            self.model.fit(X_train_scaled, y_train)
            
            # Evaluate
            train_score = self.model.score(X_train_scaled, y_train)
            test_score = self.model.score(X_test_scaled, y_test)
            
            y_pred = self.model.predict(X_test_scaled)
            
            print(f"✅ Classifier trained successfully!")
            print(f"   Train Accuracy: {train_score:.4f}")
            print(f"   Test Accuracy: {test_score:.4f}")
            
            # Save model
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            joblib.dump({
                'model': self.model,
                'scaler': self.scaler,
                'training_date': datetime.now().isoformat(),
                'classes': self.model.classes_.tolist()
            }, self.model_path)
            
            self.is_trained = True
            
        except Exception as e:
            print(f"❌ Error training classifier: {e}")
            self.is_trained = False
    
    def _load_model(self):
        """Load pre-trained model from disk."""
        try:
            data = joblib.load(self.model_path)
            self.model = data['model']
            self.scaler = data['scaler']
            self.is_trained = True
            print(f"✅ Loaded pre-trained game difficulty classifier")
        except Exception as e:
            print(f"⚠️ Could not load model: {e}. Will retrain.")
            self._train_model()
    
    def classify_game(self, min_ram_gb: int, min_vram_gb: int, 
                     min_cpu_cores: int, game_name: str = "Unknown") -> dict:
        """
        Classify game difficulty based on hardware requirements.
        
        Args:
            min_ram_gb: Minimum RAM in GB
            min_vram_gb: Minimum VRAM in GB
            min_cpu_cores: Minimum CPU cores
            game_name: Game name (for logging)
        
        Returns:
            {
                'difficulty': str ('Light', 'Medium', 'Heavy'),
                'confidence': float (0-1),
                'explanation': str,
                'recommendation': str,
                'model': str
            }
        """
        if not self.is_trained or not HAS_SKLEARN:
            return self._fallback_classification(min_ram_gb, min_vram_gb, min_cpu_cores)
        
        try:
            # Prepare features
            features = np.array([[min_ram_gb, min_vram_gb, min_cpu_cores]])
            features_scaled = self.scaler.transform(features)
            
            # Get probabilities
            probabilities = self.model.predict_proba(features_scaled)[0]
            classes = self.model.classes_
            
            # Get prediction
            prediction = self.model.predict(features_scaled)[0]
            confidence = max(probabilities)
            
            # Generate explanation
            explanations = {
                'Light': f'✅ Runs on budget PCs. RAM: {min_ram_gb}GB, GPU: {min_vram_gb}GB',
                'Medium': f'⚡ Moderate requirements. RAM: {min_ram_gb}GB, GPU: {min_vram_gb}GB',
                'Heavy': f'🔥 Demanding game. RAM: {min_ram_gb}GB, GPU: {min_vram_gb}GB, Cores: {min_cpu_cores}'
            }
            
            recommendations = {
                'Light': 'Budget build: ₹30K-50K',
                'Medium': 'Mid-range build: ₹60K-90K',
                'Heavy': 'High-end build: ₹100K+'
            }
            
            return {
                'difficulty': prediction,
                'confidence': round(confidence, 2),
                'explanation': explanations.get(prediction, 'Unknown'),
                'recommendation': recommendations.get(prediction, 'Consult recommendation service'),
                'probabilities': {c: round(p, 2) for c, p in zip(classes, probabilities)},
                'model': 'Gradient Boosting',
                'game_name': game_name
            }
        
        except Exception as e:
            print(f"Error in classification: {e}")
            return self._fallback_classification(min_ram_gb, min_vram_gb, min_cpu_cores)
    
    def _fallback_classification(self, ram: int, vram: int, cores: int) -> dict:
        """Fallback classification using simple rules."""
        if ram < 6 or vram < 2:
            difficulty = 'Light'
        elif ram < 16 or vram < 6:
            difficulty = 'Medium'
        else:
            difficulty = 'Heavy'
        
        recommendations = {
            'Light': 'Budget build: ₹30K-50K',
            'Medium': 'Mid-range build: ₹60K-90K',
            'Heavy': 'High-end build: ₹100K+'
        }
        
        return {
            'difficulty': difficulty,
            'confidence': 0.65,
            'explanation': f'RAM: {ram}GB, VRAM: {vram}GB, Cores: {cores}',
            'recommendation': recommendations[difficulty],
            'probabilities': {'Light': 0.33, 'Medium': 0.33, 'Heavy': 0.33},
            'model': 'Rule-based Fallback'
        }

# Global instance
_classifier = None

def get_game_classifier():
    """Get or create classifier instance."""
    global _classifier
    if _classifier is None:
        _classifier = GameDifficultyClassifier()
    return _classifier
