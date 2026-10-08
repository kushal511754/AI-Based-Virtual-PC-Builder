"""
ML-based price predictor using Linear Regression and Decision Tree algorithms.
Fast, lightweight, integrates with existing PC builder.
Predicts component prices based on specs.
"""

import json
import numpy as np
from datetime import datetime, timedelta
import os

class MLPricePredictor:
    """
    Machine Learning price prediction using multiple algorithms:
    - Linear Regression: For linear trends
    - Decision Tree: For non-linear relationships
    - Ensemble: Combines both for better accuracy
    """
    
    def __init__(self):
        """Initialize predictor with pre-trained models."""
        self.models_trained = False
        self.lr_model = None
        self.dt_model = None
        self.feature_scaler = None
        self.price_history = {}
        self.train_models()
    
    def train_models(self):
        """Train ML models with realistic PC component data."""
        try:
            # Synthetic training data based on real market trends
            # CPU: price vs cores, clock speed, generation
            cpu_data = [
                {'cores': 2, 'ghz': 3.5, 'generation': 10, 'price': 8000},
                {'cores': 4, 'ghz': 3.8, 'generation': 10, 'price': 12000},
                {'cores': 4, 'ghz': 4.2, 'generation': 12, 'price': 15000},
                {'cores': 6, 'ghz': 4.5, 'generation': 12, 'price': 18000},
                {'cores': 8, 'ghz': 4.8, 'generation': 12, 'price': 28000},
                {'cores': 8, 'ghz': 5.2, 'generation': 13, 'price': 32000},
                {'cores': 10, 'ghz': 5.5, 'generation': 13, 'price': 45000},
                {'cores': 12, 'ghz': 5.8, 'generation': 13, 'price': 55000},
                {'cores': 16, 'ghz': 6.0, 'generation': 13, 'price': 75000},
            ]
            
            # GPU: price vs vram, memory bus, generation
            gpu_data = [
                {'vram': 2, 'memory_bus': 64, 'generation': 10, 'price': 8000},
                {'vram': 4, 'memory_bus': 128, 'generation': 10, 'price': 16000},
                {'vram': 4, 'memory_bus': 128, 'generation': 20, 'price': 18000},
                {'vram': 6, 'memory_bus': 192, 'generation': 20, 'price': 28000},
                {'vram': 8, 'memory_bus': 256, 'generation': 30, 'price': 40000},
                {'vram': 10, 'memory_bus': 320, 'generation': 30, 'price': 55000},
                {'vram': 12, 'memory_bus': 384, 'generation': 40, 'price': 75000},
                {'vram': 16, 'memory_bus': 512, 'generation': 40, 'price': 95000},
            ]
            
            # RAM: price vs capacity, speed, type
            ram_data = [
                {'capacity': 4, 'speed': 2400, 'type': 1, 'price': 2000},
                {'capacity': 8, 'speed': 3000, 'type': 1, 'price': 4000},
                {'capacity': 8, 'speed': 3600, 'type': 1, 'price': 5000},
                {'capacity': 16, 'speed': 3600, 'type': 1, 'price': 8000},
                {'capacity': 16, 'speed': 5200, 'type': 2, 'price': 10000},
                {'capacity': 32, 'speed': 5200, 'type': 2, 'price': 18000},
                {'capacity': 64, 'speed': 6000, 'type': 2, 'price': 35000},
            ]
            
            # Storage: price vs capacity, speed
            storage_data = [
                {'capacity': 256, 'speed': 500, 'price': 2000},
                {'capacity': 512, 'speed': 1500, 'price': 4000},
                {'capacity': 512, 'speed': 3500, 'price': 5000},
                {'capacity': 1000, 'speed': 3500, 'price': 8000},
                {'capacity': 2000, 'speed': 5000, 'price': 15000},
                {'capacity': 4000, 'speed': 5000, 'price': 28000},
            ]
            
            # Train models for each component type
            self.cpu_model = self._train_ensemble_model(cpu_data, ['cores', 'ghz', 'generation'], 'price')
            self.gpu_model = self._train_ensemble_model(gpu_data, ['vram', 'memory_bus', 'generation'], 'price')
            self.ram_model = self._train_ensemble_model(ram_data, ['capacity', 'speed', 'type'], 'price')
            self.storage_model = self._train_ensemble_model(storage_data, ['capacity', 'speed'], 'price')
            
            self.models_trained = True
            # Models trained successfully
            
        except Exception as e:
            self.models_trained = False
            # Model training error silently handled
    
    def _train_ensemble_model(self, data, feature_keys, target_key):
        """Train ensemble of Linear Regression and Decision Tree."""
        try:
            X = np.array([[item[k] for k in feature_keys] for item in data])
            y = np.array([item[target_key] for item in data])
            
            # Normalize features (0-1 scale)
            X_min = X.min(axis=0)
            X_max = X.max(axis=0)
            X_normalized = (X - X_min) / (X_max - X_min + 1e-8)
            
            # Linear Regression: y = w*x + b
            # Using normal equation: w = (X^T * X)^-1 * X^T * y
            ones = np.ones((X_normalized.shape[0], 1))
            X_with_bias = np.hstack([ones, X_normalized])
            
            try:
                weights = np.linalg.lstsq(X_with_bias, y, rcond=None)[0]
            except:
                weights = np.array([y.mean()] + [0] * X_normalized.shape[1])
            
            # Decision Tree: Simple depth-2 tree using median splits
            dt_tree = self._build_simple_tree(X_normalized, y, depth=0, max_depth=2)
            
            return {
                'type': 'ensemble',
                'lr_weights': weights.tolist(),
                'dt_tree': dt_tree,
                'feature_keys': feature_keys,
                'X_min': X_min.tolist(),
                'X_max': X_max.tolist(),
                'y_mean': float(y.mean()),
                'y_std': float(y.std())
            }
        except Exception as e:
            print(f"Error training model: {e}")
            return None
    
    def _build_simple_tree(self, X, y, depth=0, max_depth=2):
        """Build simple decision tree recursively."""
        if depth >= max_depth or len(y) <= 2 or len(np.unique(y)) == 1:
            return {'type': 'leaf', 'value': float(y.mean())}
        
        best_split = None
        best_gain = 0
        
        # Try splitting on each feature
        for feature_idx in range(X.shape[1]):
            # Use median as split point
            split_value = np.median(X[:, feature_idx])
            
            left_mask = X[:, feature_idx] <= split_value
            right_mask = ~left_mask
            
            if left_mask.sum() == 0 or right_mask.sum() == 0:
                continue
            
            # Information gain (variance reduction)
            parent_variance = np.var(y)
            left_variance = np.var(y[left_mask])
            right_variance = np.var(y[right_mask])
            
            gain = parent_variance - (left_mask.sum() * left_variance + right_mask.sum() * right_variance) / len(y)
            
            if gain > best_gain:
                best_gain = gain
                best_split = {
                    'feature': int(feature_idx),
                    'value': float(split_value),
                    'left_indices': np.where(left_mask)[0].tolist(),
                    'right_indices': np.where(right_mask)[0].tolist(),
                    'left_y': y[left_mask].tolist(),
                    'right_y': y[right_mask].tolist()
                }
        
        if best_split is None:
            return {'type': 'leaf', 'value': float(y.mean())}
        
        return {
            'type': 'node',
            'feature': best_split['feature'],
            'value': best_split['value'],
            'left': self._build_simple_tree(X[best_split['left_indices']], 
                                           np.array(best_split['left_y']), 
                                           depth+1, max_depth),
            'right': self._build_simple_tree(X[best_split['right_indices']], 
                                            np.array(best_split['right_y']), 
                                            depth+1, max_depth)
        }
    
    def predict_cpu_price(self, cores, ghz, generation=13):
        """Predict CPU price using ML model."""
        if not self.cpu_model:
            return self._estimate_cpu_price(cores, ghz, generation)
        
        features = np.array([[cores, ghz, generation]])
        return self._predict_with_ensemble(features, self.cpu_model)
    
    def predict_gpu_price(self, vram, memory_bus, generation=40):
        """Predict GPU price using ML model."""
        if not self.gpu_model:
            return self._estimate_gpu_price(vram, memory_bus, generation)
        
        features = np.array([[vram, memory_bus, generation]])
        return self._predict_with_ensemble(features, self.gpu_model)
    
    def predict_ram_price(self, capacity, speed, ram_type=2):
        """Predict RAM price using ML model."""
        if not self.ram_model:
            return self._estimate_ram_price(capacity, speed, ram_type)
        
        features = np.array([[capacity, speed, ram_type]])
        return self._predict_with_ensemble(features, self.ram_model)
    
    def predict_storage_price(self, capacity, speed=3500):
        """Predict storage price using ML model."""
        if not self.storage_model:
            return self._estimate_storage_price(capacity, speed)
        
        features = np.array([[capacity, speed]])
        return self._predict_with_ensemble(features, self.storage_model)
    
    def _predict_with_ensemble(self, features, model):
        """Make prediction using ensemble (Linear Regression + Decision Tree)."""
        try:
            # Normalize features
            X_min = np.array(model['X_min'])
            X_max = np.array(model['X_max'])
            X_norm = (features - X_min) / (X_max - X_min + 1e-8)
            
            # Linear Regression prediction
            ones = np.ones((X_norm.shape[0], 1))
            X_with_bias = np.hstack([ones, X_norm])
            lr_pred = X_with_bias @ np.array(model['lr_weights'])
            
            # Decision Tree prediction
            dt_pred = np.array([self._traverse_tree(x, model['dt_tree']) for x in X_norm])
            
            # Ensemble: average both predictions
            ensemble_pred = (lr_pred + dt_pred) / 2
            
            # Ensure positive price
            return max(float(ensemble_pred[0]), 1000)
        except Exception as e:
            print(f"Prediction error: {e}")
            return 5000
    
    def _traverse_tree(self, features, node):
        """Traverse decision tree to get prediction."""
        if node['type'] == 'leaf':
            return node['value']
        
        feature_idx = node['feature']
        threshold = node['value']
        
        if features[feature_idx] <= threshold:
            return self._traverse_tree(features, node['left'])
        else:
            return self._traverse_tree(features, node['right'])
    
    def _estimate_cpu_price(self, cores, ghz, generation=13):
        """Fallback: Linear estimation without ML."""
        base_price = 8000
        price_per_core = 5000
        price_per_ghz = 2000
        generation_multiplier = 1 + (generation - 10) * 0.08
        
        price = (base_price + cores * price_per_core + ghz * price_per_ghz) * generation_multiplier
        return max(price, 5000)
    
    def _estimate_gpu_price(self, vram, memory_bus, generation=40):
        """Fallback: Linear estimation without ML."""
        base_price = 5000
        price_per_vram = 8000
        price_per_bus = 50
        generation_multiplier = 1 + (generation - 10) * 0.12
        
        price = (base_price + vram * price_per_vram + memory_bus * price_per_bus) * generation_multiplier
        return max(price, 5000)
    
    def _estimate_ram_price(self, capacity, speed, ram_type=2):
        """Fallback: Linear estimation without ML."""
        base_price = 1000
        price_per_gb = 400
        type_multiplier = 0.8 if ram_type == 1 else 1.2
        speed_multiplier = 1 + (speed - 2400) / 1000 * 0.1
        
        price = (base_price + capacity * price_per_gb) * type_multiplier * speed_multiplier
        return max(price, 500)
    
    def _estimate_storage_price(self, capacity, speed=3500):
        """Fallback: Linear estimation without ML."""
        base_price = 1500
        price_per_gb = 4
        speed_multiplier = 1 + (speed - 500) / 1000 * 0.15
        
        price = (base_price + capacity * price_per_gb) * speed_multiplier
        return max(price, 1000)
    
    def predict_total_build_cost(self, cpu_specs, gpu_specs, ram_specs, storage_specs):
        """Predict total build cost using individual component predictions."""
        cpu_price = self.predict_cpu_price(
            cpu_specs.get('cores', 8),
            cpu_specs.get('ghz', 4.5),
            cpu_specs.get('generation', 13)
        )
        
        gpu_price = self.predict_gpu_price(
            gpu_specs.get('vram', 6),
            gpu_specs.get('memory_bus', 192),
            gpu_specs.get('generation', 40)
        )
        
        ram_price = self.predict_ram_price(
            ram_specs.get('capacity', 16),
            ram_specs.get('speed', 5200),
            ram_specs.get('type', 2)
        )
        
        storage_price = self.predict_storage_price(
            storage_specs.get('capacity', 512),
            storage_specs.get('speed', 3500)
        )
        
        # Add other components (motherboard, PSU, case, cooling)
        other_components = 12000 + 5000 + 4000 + 3000  # Rough estimates
        
        total = cpu_price + gpu_price + ram_price + storage_price + other_components
        
        return {
            'cpu_price': round(cpu_price, 2),
            'gpu_price': round(gpu_price, 2),
            'ram_price': round(ram_price, 2),
            'storage_price': round(storage_price, 2),
            'other_components': other_components,
            'total': round(total, 2),
            'currency': 'INR'
        }

# Global instance
_price_predictor = None

def get_price_predictor():
    """Get or create global ML price predictor instance."""
    global _price_predictor
    if _price_predictor is None:
        _price_predictor = MLPricePredictor()
    return _price_predictor
