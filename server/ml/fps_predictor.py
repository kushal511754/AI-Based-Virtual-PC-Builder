"""
ML Model: FPS Prediction Model
Predicts gaming FPS based on game requirements and PC specifications.
Uses: Neural Network (if TensorFlow available) or Gradient Boosting as fallback
"""

import os
import numpy as np
import joblib
from datetime import datetime

try:
    from sklearn.ensemble import GradientBoostingRegressor
    from sklearn.preprocessing import StandardScaler
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import mean_absolute_error, r2_score
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False

try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import layers
    HAS_TENSORFLOW = True
except ImportError:
    HAS_TENSORFLOW = False

class FPSPredictor:
    """
    Predicts FPS (frames per second) based on:
    - Game requirements (min RAM, min VRAM, min cores)
    - PC specifications (actual RAM, VRAM, CPU cores, GPU VRAM)
    - Resolution and graphics settings
    
    Returns estimated FPS at 1080p, 1440p, and 4K resolutions.
    """
    
    # Training data: (game_req_ram, game_req_vram, game_req_cores, 
    #                 pc_ram, pc_vram, pc_cores, fps_1080p_high, fps_1440p_high, fps_4k_high)
    TRAINING_DATA = [
        # Light games (Valorant, CS:GO, etc.)
        (4, 1, 2, 8, 2, 4, 240, 180, 120),
        (4, 1, 2, 8, 4, 4, 240, 200, 140),
        (4, 1, 2, 16, 6, 8, 280, 240, 160),
        
        # Medium games (Fortnite, GTA V, etc.)
        (8, 3, 4, 8, 4, 4, 100, 70, 40),
        (8, 3, 4, 16, 6, 8, 140, 100, 60),
        (8, 3, 4, 16, 8, 8, 160, 120, 80),
        (8, 4, 6, 16, 8, 8, 120, 90, 60),
        (8, 4, 6, 32, 10, 12, 165, 144, 100),
        
        # Heavy games (Cyberpunk, Elden Ring, etc.)
        (16, 8, 8, 16, 8, 8, 70, 50, 30),
        (16, 8, 8, 32, 12, 12, 100, 80, 50),
        (16, 8, 8, 32, 16, 16, 140, 110, 70),
        (16, 12, 12, 32, 16, 16, 120, 100, 60),
        (32, 16, 16, 64, 24, 24, 160, 144, 90),
    ]
    
    def __init__(self, model_path='server/ml/models/fps_predictor.pkl',
                 use_neural=False):
        """Initialize FPS predictor."""
        self.model_path = model_path
        self.scaler = None
        self.model = None
        self.is_trained = False
        self.use_neural = use_neural and HAS_TENSORFLOW
        
        if not HAS_SKLEARN:
            print("⚠️ scikit-learn not installed. FPS prediction will use fallback mode.")
            return
        
        # Try to load pre-trained model
        if os.path.exists(model_path):
            self._load_model()
        else:
            self._train_model()
    
    def _train_model(self):
        """Train FPS prediction model."""
        if not HAS_SKLEARN:
            return
        
        try:
            print("🔧 Training FPS Prediction Model...")
            
            # Prepare training data
            X_list = []
            y_list_1080p = []
            y_list_1440p = []
            y_list_4k = []
            
            for game_ram, game_vram, game_cores, pc_ram, pc_vram, pc_cores, fps_1080, fps_1440, fps_4k in self.TRAINING_DATA:
                X_list.append([game_ram, game_vram, game_cores, pc_ram, pc_vram, pc_cores])
                y_list_1080p.append(fps_1080)
                y_list_1440p.append(fps_1440)
                y_list_4k.append(fps_4k)
            
            X = np.array(X_list)
            
            # Split data
            X_train, X_test, y_1080_train, y_1080_test = train_test_split(
                X, np.array(y_list_1080p), test_size=0.2, random_state=42
            )
            _, _, y_1440_train, y_1440_test = train_test_split(
                X, np.array(y_list_1440p), test_size=0.2, random_state=42
            )
            _, _, y_4k_train, y_4k_test = train_test_split(
                X, np.array(y_list_4k), test_size=0.2, random_state=42
            )
            
            # Scale features
            self.scaler = StandardScaler()
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            # Train separate models for each resolution
            models = {}
            for res_name, y_train, y_test in [
                ('1080p', y_1080_train, y_1080_test),
                ('1440p', y_1440_train, y_1440_test),
                ('4k', y_4k_train, y_4k_test)
            ]:
                model = GradientBoostingRegressor(
                    n_estimators=100,
                    max_depth=5,
                    learning_rate=0.1,
                    random_state=42
                )
                
                model.fit(X_train_scaled, y_train)
                
                test_score = model.score(X_test_scaled, y_test)
                y_pred = model.predict(X_test_scaled)
                mae = mean_absolute_error(y_test, y_pred)
                
                models[res_name] = model
                print(f"   {res_name}: R² = {test_score:.4f}, MAE = {mae:.1f} FPS")
            
            self.model = models
            print(f"✅ FPS Predictor trained successfully!")
            
            # Save model
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            joblib.dump({
                'models': self.model,
                'scaler': self.scaler,
                'training_date': datetime.now().isoformat()
            }, self.model_path)
            
            self.is_trained = True
            
        except Exception as e:
            print(f"❌ Error training FPS model: {e}")
            self.is_trained = False
    
    def _load_model(self):
        """Load pre-trained model."""
        try:
            data = joblib.load(self.model_path)
            self.model = data['models']
            self.scaler = data['scaler']
            self.is_trained = True
            print(f"✅ Loaded pre-trained FPS predictor")
        except Exception as e:
            print(f"⚠️ Could not load model: {e}. Will retrain.")
            self._train_model()
    
    def predict_fps(self, game_name: str, game_min_ram: int, game_min_vram: int,
                   game_min_cores: int, pc_ram: int, pc_vram: int, 
                   pc_cores: int) -> dict:
        """
        Predict FPS for a game on given PC specifications.
        
        Args:
            game_name: Name of the game
            game_min_ram: Game's minimum RAM requirement
            game_min_vram: Game's minimum VRAM requirement
            game_min_cores: Game's minimum CPU cores
            pc_ram: PC actual RAM
            pc_vram: PC actual VRAM
            pc_cores: PC actual CPU cores
        
        Returns:
            {
                'fps_1080p': int,
                'fps_1440p': int,
                'fps_4k': int,
                'recommended_resolution': str,
                'confidence': float,
                'performance_tier': str,
                'game_name': str
            }
        """
        if not self.is_trained or not HAS_SKLEARN:
            return self._fallback_fps(game_min_ram, game_min_vram, 
                                     game_min_cores, pc_ram, pc_vram, pc_cores)
        
        try:
            # Prepare features
            features = np.array([[game_min_ram, game_min_vram, game_min_cores,
                                pc_ram, pc_vram, pc_cores]])
            features_scaled = self.scaler.transform(features)
            
            # Predict for each resolution
            fps_1080p = int(max(30, self.model['1080p'].predict(features_scaled)[0]))
            fps_1440p = int(max(20, self.model['1440p'].predict(features_scaled)[0]))
            fps_4k = int(max(15, self.model['4k'].predict(features_scaled)[0]))
            
            # Determine recommended resolution based on FPS
            if fps_4k > 60:
                rec_resolution = '4K Ultra 60fps'
            elif fps_1440p > 100:
                rec_resolution = '1440p Ultra 100+fps'
            elif fps_1440p > 60:
                rec_resolution = '1440p High 60fps'
            elif fps_1080p > 100:
                rec_resolution = '1080p Ultra 100+fps'
            else:
                rec_resolution = '1080p High 60fps'
            
            # Determine performance tier
            if fps_1080p < 60:
                tier = 'Below Recommended'
            elif fps_1440p < 60:
                tier = 'Good for 1080p'
            elif fps_4k > 60:
                tier = 'Excellent (4K Ready)'
            else:
                tier = 'Great for 1440p'
            
            return {
                'fps_1080p_high': fps_1080p,
                'fps_1440p_high': fps_1440p,
                'fps_4k_high': fps_4k,
                'recommended_resolution': rec_resolution,
                'confidence': 0.85,
                'performance_tier': tier,
                'game_name': game_name,
                'model': 'Gradient Boosting Ensemble'
            }
        
        except Exception as e:
            print(f"Error in FPS prediction: {e}")
            return self._fallback_fps(game_min_ram, game_min_vram,
                                     game_min_cores, pc_ram, pc_vram, pc_cores)
    
    def _fallback_fps(self, game_min_ram, game_min_vram, game_min_cores,
                     pc_ram, pc_vram, pc_cores) -> dict:
        """Fallback FPS estimation using simple ratio."""
        # Calculate performance ratio
        ram_ratio = min(1.0, pc_ram / max(game_min_ram, 1))
        vram_ratio = min(1.0, pc_vram / max(game_min_vram, 1))
        core_ratio = min(1.0, pc_cores / max(game_min_cores, 1))
        
        # Average ratio
        overall_ratio = (ram_ratio + vram_ratio + core_ratio) / 3
        
        # Base FPS values
        base_1080p = 75
        base_1440p = 55
        base_4k = 35
        
        # Apply ratio
        fps_1080p = int(base_1080p * overall_ratio)
        fps_1440p = int(base_1440p * overall_ratio)
        fps_4k = int(base_4k * overall_ratio)
        
        if fps_1080p < 60:
            tier = 'Below Recommended'
            rec = '1080p Medium'
        elif fps_1440p < 60:
            tier = 'Good for 1080p'
            rec = '1080p High'
        else:
            tier = 'Great'
            rec = '1440p High'
        
        return {
            'fps_1080p_high': max(15, fps_1080p),
            'fps_1440p_high': max(10, fps_1440p),
            'fps_4k_high': max(5, fps_4k),
            'recommended_resolution': rec,
            'confidence': 0.60,
            'performance_tier': tier,
            'model': 'Heuristic-based'
        }

# Global instance
_fps_predictor = None

def get_fps_predictor():
    """Get or create FPS predictor instance."""
    global _fps_predictor
    if _fps_predictor is None:
        _fps_predictor = FPSPredictor()
    return _fps_predictor
