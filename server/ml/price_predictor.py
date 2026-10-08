"""
ML Model: Component Price Prediction
Predicts future component prices based on historical trends and specifications.
Uses: Random Forest Regressor with historical Indian market data
"""

import os
import json
import pickle
import numpy as np
from datetime import datetime, timedelta
import joblib

# Try to import ML libraries
try:
    from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
    from sklearn.preprocessing import StandardScaler, LabelEncoder
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import mean_absolute_error, r2_score
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False

class PricePredictor:
    """
    Predicts component prices using machine learning.
    Trained on historical gaming PC component prices from Indian market.
    """
    
    # Historical price data (Indian market, 2022-2025)
    TRAINING_DATA = {
        'cpu': [
            # (name, cores, ghz, release_date_days_ago, actual_price_inr, trend_direction)
            ('Intel i3-12100', 4, 3.3, 700, 8500, -0.15),
            ('Intel i5-12400', 6, 3.4, 650, 15200, -0.12),
            ('Intel i7-12700', 12, 3.6, 600, 28000, -0.1),
            ('Intel i9-13900K', 24, 3.0, 400, 65000, -0.05),
            ('AMD Ryzen 5 5600X', 6, 3.7, 800, 14500, -0.18),
            ('AMD Ryzen 7 5800X', 8, 3.8, 750, 25000, -0.14),
            ('AMD Ryzen 9 5950X', 16, 3.4, 700, 45000, -0.12),
            ('Intel i5-13600K', 14, 3.5, 300, 32000, -0.08),
            ('Intel i7-13700K', 16, 3.4, 250, 48000, -0.06),
        ],
        'gpu': [
            # (name, vram_gb, cuda_cores, release_date_days_ago, actual_price_inr, trend_direction)
            ('GTX 1650', 4, 896, 600, 12500, -0.2),
            ('RTX 2060', 6, 1920, 900, 18500, -0.22),
            ('RTX 2070', 8, 2304, 850, 32000, -0.18),
            ('RTX 3060', 12, 3584, 400, 28000, -0.15),
            ('RTX 3070', 8, 5888, 350, 48000, -0.12),
            ('RTX 3080', 10, 8704, 300, 75000, -0.1),
            ('RTX 4070', 12, 5888, 150, 52000, -0.08),
            ('RTX 4080', 16, 9728, 100, 89000, -0.05),
            ('RTX 4090', 24, 16384, 80, 185000, -0.03),
            ('RX 6700', 12, 2304, 350, 26000, -0.16),
            ('RX 6800', 16, 3840, 300, 42000, -0.14),
        ],
        'ram': [
            # (name, capacity_gb, speed_mhz, release_date_days_ago, actual_price_inr, trend_direction)
            ('DDR4 8GB 3200MHz', 8, 3200, 600, 2500, -0.25),
            ('DDR4 16GB 3600MHz', 16, 3600, 500, 5200, -0.22),
            ('DDR4 32GB 3600MHz', 32, 3600, 400, 10500, -0.2),
            ('DDR5 16GB 5600MHz', 16, 5600, 300, 7500, -0.15),
            ('DDR5 32GB 5600MHz', 32, 5600, 250, 15000, -0.12),
            ('DDR5 64GB 5600MHz', 64, 5600, 150, 30000, -0.1),
        ],
        'storage': [
            # (name, capacity_gb, speed_mbps, release_date_days_ago, actual_price_inr, trend_direction)
            ('SSD 256GB NVMe', 256, 3500, 500, 2000, -0.3),
            ('SSD 512GB NVMe', 512, 3500, 450, 4000, -0.28),
            ('SSD 1TB NVMe', 1000, 3500, 400, 6500, -0.25),
            ('SSD 2TB NVMe', 2000, 3500, 300, 13000, -0.2),
            ('HDD 2TB SATA', 2000, 150, 600, 4500, -0.4),
            ('HDD 4TB SATA', 4000, 150, 500, 8000, -0.38),
        ],
    }
    
    def __init__(self, model_path='server/ml/models/price_predictor.pkl'):
        """Initialize price predictor with trained model."""
        self.model_path = model_path
        self.scaler = None
        self.model = None
        self.feature_names = ['cores_or_vram', 'clock_speed', 'age_days', 'trend']
        self.is_trained = False
        
        if not HAS_SKLEARN:
            print("⚠️ scikit-learn not installed. Price prediction will use fallback mode.")
            return
        
        # Try to load pre-trained model
        if os.path.exists(model_path):
            self._load_model()
        else:
            # Train a new model
            self._train_model()
    
    def _train_model(self):
        """Train Random Forest model on historical data."""
        if not HAS_SKLEARN:
            return
        
        try:
            print("🔧 Training Price Prediction Model...")
            
            # Prepare training data from all components
            X_list = []
            y_list = []
            
            for component_type, data in self.TRAINING_DATA.items():
                for item in data:
                    name, attr1, attr2, days_ago, price, trend = item
                    X_list.append([attr1, attr2, days_ago, trend])
                    y_list.append(price)
            
            X = np.array(X_list)
            y = np.array(y_list)
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Scale features
            self.scaler = StandardScaler()
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            # Train Random Forest
            self.model = RandomForestRegressor(
                n_estimators=100,
                max_depth=15,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42,
                n_jobs=-1
            )
            
            self.model.fit(X_train_scaled, y_train)
            
            # Evaluate
            train_score = self.model.score(X_train_scaled, y_train)
            test_score = self.model.score(X_test_scaled, y_test)
            
            y_pred = self.model.predict(X_test_scaled)
            mae = mean_absolute_error(y_test, y_pred)
            
            print(f"✅ Model trained successfully!")
            print(f"   Train R² Score: {train_score:.4f}")
            print(f"   Test R² Score: {test_score:.4f}")
            print(f"   Mean Absolute Error: ₹{mae:.0f}")
            
            # Save model
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            joblib.dump({
                'model': self.model,
                'scaler': self.scaler,
                'training_date': datetime.now().isoformat()
            }, self.model_path)
            
            self.is_trained = True
            
        except Exception as e:
            print(f"❌ Error training model: {e}")
            self.is_trained = False
    
    def _load_model(self):
        """Load pre-trained model from disk."""
        try:
            data = joblib.load(self.model_path)
            self.model = data['model']
            self.scaler = data['scaler']
            self.is_trained = True
            print(f"✅ Loaded pre-trained price predictor model")
        except Exception as e:
            print(f"⚠️ Could not load model: {e}. Will retrain.")
            self._train_model()
    
    def predict_price(self, component_type: str, cores_or_vram: int, 
                     clock_speed: float, days_old: int = 0) -> dict:
        """
        Predict current price of a component.
        
        Args:
            component_type: 'cpu', 'gpu', 'ram', 'storage'
            cores_or_vram: Number of cores (CPU) or VRAM GB (GPU)
            clock_speed: Clock speed in GHz or speed in MHz
            days_old: How many days old is the component (0 = latest)
        
        Returns:
            {
                'predicted_price_inr': float,
                'confidence': float (0-1),
                'price_trend': str ('increasing', 'stable', 'decreasing'),
                'recommendation': str
            }
        """
        if not self.is_trained or not HAS_SKLEARN:
            return self._fallback_price(cores_or_vram)
        
        try:
            # Determine trend based on component age
            if days_old < 100:
                trend = 0.05  # New components: slight increase
            elif days_old < 500:
                trend = -0.10  # Mid-age: slight decrease
            else:
                trend = -0.25  # Old: strong decrease
            
            # Prepare features
            features = np.array([[cores_or_vram, clock_speed, days_old, trend]])
            features_scaled = self.scaler.transform(features)
            
            # Predict
            predicted_price = self.model.predict(features_scaled)[0]
            predicted_price = max(predicted_price, 0)  # Ensure positive
            
            # Calculate confidence based on feature range
            confidence = min(0.95, max(0.70, 1.0 - (abs(trend) / 2)))
            
            # Determine trend
            if trend > 0.02:
                price_trend = 'increasing'
            elif trend < -0.15:
                price_trend = 'decreasing'
            else:
                price_trend = 'stable'
            
            # Generate recommendation
            if predicted_price > 80000:
                recommendation = 'Premium tier - Consider alternatives for budget builds'
            elif predicted_price > 50000:
                recommendation = 'Mid-to-high tier - Good for high-end gaming'
            elif predicted_price > 20000:
                recommendation = 'Mid-range - Suitable for most builds'
            else:
                recommendation = 'Budget-friendly - Great value for entry-level'
            
            return {
                'predicted_price_inr': round(predicted_price, 0),
                'confidence': round(confidence, 2),
                'price_trend': price_trend,
                'recommendation': recommendation,
                'model': 'Random Forest',
                'training_samples': len(self.TRAINING_DATA) * 5
            }
        
        except Exception as e:
            print(f"Error in prediction: {e}")
            return self._fallback_price(cores_or_vram)
    
    def _fallback_price(self, cores_or_vram: int) -> dict:
        """Fallback pricing when ML model unavailable."""
        # Simple heuristic-based pricing
        base_prices = {
            4: 8000,    # 4 cores/GB
            6: 12000,   # 6 cores/GB
            8: 16000,   # 8 cores/GB
            12: 25000,  # 12 cores/GB
            16: 40000,  # 16 cores/GB
            24: 65000,  # 24 cores/GB
        }
        
        # Find closest tier
        closest = min(base_prices.keys(), key=lambda x: abs(x - cores_or_vram))
        predicted = base_prices[closest] * (cores_or_vram / closest)
        
        return {
            'predicted_price_inr': round(predicted, 0),
            'confidence': 0.60,
            'price_trend': 'unknown',
            'recommendation': 'Fallback pricing - Limited data',
            'model': 'Heuristic',
            'training_samples': 0
        }

# Global instance
_price_predictor = None

def get_price_predictor():
    """Get or create price predictor instance."""
    global _price_predictor
    if _price_predictor is None:
        _price_predictor = PricePredictor()
    return _price_predictor
