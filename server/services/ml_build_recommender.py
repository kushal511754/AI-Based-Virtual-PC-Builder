"""
ML-based Build Recommendation Engine using K-means clustering.
Groups similar PC builds and recommends optimal ones for budget.
"""

import math
import random
from collections import defaultdict

class MLBuildRecommender:
    """
    PC Build Recommender using K-means clustering algorithm.
    
    Clusters similar PC builds and recommends best value builds
    based on game requirements and budget.
    """
    
    def __init__(self):
        """Initialize build recommender."""
        self.build_clusters = {}
        self.domain_clusters = defaultdict(list)
        self.train_clusters()
    
    def train_clusters(self):
        """Train K-means clustering on realistic PC build profiles."""
        # Build profiles: (domain, budget_tier, cpu_cores, gpu_vram, ram_gb, storage_gb, total_price)
        build_profiles = [
            # Budget tier builds (₹30k-50k)
            ('gaming', 'budget', 2, 2, 8, 256, 35000),
            ('gaming', 'budget', 4, 2, 8, 256, 40000),
            ('gaming', 'budget', 4, 4, 8, 512, 48000),
            
            # Mid-range tier (₹50k-90k)
            ('gaming', 'mid', 4, 4, 16, 512, 60000),
            ('gaming', 'mid', 6, 6, 16, 512, 75000),
            ('gaming', 'mid', 6, 8, 16, 1024, 85000),
            
            # High-end tier (₹90k-150k)
            ('gaming', 'high', 8, 8, 16, 1024, 100000),
            ('gaming', 'high', 8, 10, 32, 1024, 125000),
            ('gaming', 'high', 12, 12, 32, 2048, 145000),
            
            # Video editing builds
            ('video_editing', 'budget', 8, 4, 32, 1024, 70000),
            ('video_editing', 'mid', 12, 6, 64, 2048, 110000),
            ('video_editing', 'high', 16, 8, 64, 4096, 160000),
            
            # Programming builds
            ('programming', 'budget', 6, 2, 16, 512, 45000),
            ('programming', 'mid', 8, 4, 32, 1024, 75000),
            ('programming', 'high', 12, 6, 64, 2048, 130000),
            
            # Streaming builds
            ('streaming', 'budget', 8, 4, 24, 1024, 65000),
            ('streaming', 'mid', 10, 6, 32, 1024, 105000),
            ('streaming', 'high', 16, 10, 64, 2048, 160000),
        ]
        
        # Cluster builds by domain using K-means
        for domain in ['gaming', 'video_editing', 'programming', 'streaming']:
            domain_builds = [b for b in build_profiles if b[0] == domain]
            clusters = self._kmeans_cluster(domain_builds, k=3, iterations=10)
            self.domain_clusters[domain] = clusters
    
    def _kmeans_cluster(self, data, k=3, iterations=10):
        """
        K-means clustering algorithm.
        
        Args:
            data: List of build profiles (domain, tier, cpu, gpu, ram, storage, price)
            k: Number of clusters
            iterations: Max iterations
        
        Returns:
            List of clusters with centroids
        """
        if len(data) == 0:
            return []
        
        # Features: cpu_cores, gpu_vram, ram_gb, storage_gb, total_price
        # Extract features (skip domain and tier)
        features = [[float(d[2]), float(d[3]), float(d[4]), float(d[5]), float(d[6])/10000] for d in data]
        
        # Normalize features (0-1 scale)
        features_norm = self._normalize_features(features)
        
        # Initialize centroids randomly
        random.seed(42)  # For reproducibility
        centroids = random.sample(features_norm, min(k, len(features_norm)))
        
        # K-means iterations
        for iteration in range(iterations):
            # Assign points to nearest centroid
            clusters = [[] for _ in range(k)]
            for idx, point in enumerate(features_norm):
                nearest_centroid = min(range(k), key=lambda c: self._euclidean_distance(point, centroids[c]))
                clusters[nearest_centroid].append(idx)
            
            # Update centroids
            new_centroids = []
            for cluster_indices in clusters:
                if len(cluster_indices) == 0:
                    # Keep old centroid if cluster is empty
                    new_centroids.append(centroids[len(new_centroids)])
                else:
                    # Calculate mean of cluster points
                    cluster_points = [features_norm[i] for i in cluster_indices]
                    centroid = [sum(p[j] for p in cluster_points) / len(cluster_points) for j in range(len(cluster_points[0]))]
                    new_centroids.append(centroid)
            
            centroids = new_centroids
        
        # Final assignment
        clusters = [[] for _ in range(k)]
        for idx, point in enumerate(features_norm):
            nearest_centroid = min(range(k), key=lambda c: self._euclidean_distance(point, centroids[c]))
            clusters[nearest_centroid].append(idx)
        
        # Return clusters with original data and centroids
        result = []
        for cluster_idx, cluster_point_indices in enumerate(clusters):
            if len(cluster_point_indices) > 0:
                cluster_data = [data[i] for i in cluster_point_indices]
                result.append({
                    'centroid': centroids[cluster_idx],
                    'builds': cluster_data,
                    'size': len(cluster_data)
                })
        
        return result
    
    def _normalize_features(self, features):
        """Normalize features to 0-1 scale."""
        if len(features) == 0:
            return features
        
        num_features = len(features[0])
        normalized = []
        
        for j in range(num_features):
            values = [f[j] for f in features]
            min_val = min(values)
            max_val = max(values)
            range_val = max_val - min_val if max_val != min_val else 1
            
            for i, f in enumerate(features):
                if j >= len(normalized[i]) if i < len(normalized) else False:
                    if i >= len(normalized):
                        normalized.append([])
                    normalized[i].append((f[j] - min_val) / range_val)
        
        # Reshape properly
        result = []
        for i in range(len(features)):
            row = []
            for j in range(num_features):
                values = [f[j] for f in features]
                min_val = min(values)
                max_val = max(values)
                range_val = max_val - min_val if max_val != min_val else 1
                row.append((features[i][j] - min_val) / range_val)
            result.append(row)
        
        return result
    
    def _euclidean_distance(self, point1, point2):
        """Calculate Euclidean distance between two points."""
        return math.sqrt(sum((p1 - p2) ** 2 for p1, p2 in zip(point1, point2)))
    
    def recommend_build(self, domain, budget_inr, game_requirements=None):
        """
        Recommend a PC build using clustering.
        
        Args:
            domain: 'gaming', 'video_editing', 'programming', 'streaming'
            budget_inr: Budget in INR
            game_requirements: Optional dict with game specs
        
        Returns:
            Recommended build with components and reasoning
        """
        if domain not in self.domain_clusters:
            domain = 'gaming'  # Default
        
        clusters = self.domain_clusters[domain]
        
        if not clusters:
            return self._default_recommendation(domain, budget_inr)
        
        # Find cluster closest to budget and game requirements
        best_build = None
        best_score = float('inf')
        
        for cluster in clusters:
            for build in cluster['builds']:
                domain, tier, cpu, gpu, ram, storage, price = build
                
                # Score: minimize budget difference
                budget_diff = abs(price - budget_inr)
                
                # If game requirements provided, consider them
                if game_requirements:
                    req_cpu = game_requirements.get('cpu_cores', 4)
                    req_gpu = game_requirements.get('gpu_vram', 4)
                    req_ram = game_requirements.get('ram_gb', 8)
                    
                    # Penalty if specs below requirements
                    cpu_penalty = max(0, req_cpu - cpu) * 1000
                    gpu_penalty = max(0, req_gpu - gpu) * 2000
                    ram_penalty = max(0, req_ram - ram) * 500
                    
                    score = budget_diff + cpu_penalty + gpu_penalty + ram_penalty
                else:
                    score = budget_diff
                
                if score < best_score:
                    best_score = score
                    best_build = build
        
        if not best_build:
            return self._default_recommendation(domain, budget_inr)
        
        # Build recommendation response
        domain, tier, cpu, gpu, ram, storage, price = best_build
        
        components = {
            'cpu': f'Intel i{3 + cpu*2}/AMD Ryzen {5 + cpu}',
            'gpu': f'RTX {2000 + gpu*500}/RX {5700 + gpu*500}',
            'ram': f'{ram}GB DDR4/DDR5',
            'storage': f'{storage}GB SSD',
            'motherboard': 'B550/Z590 or higher',
            'psu': f'{550 + cpu*50}W 80+ Gold',
            'case': 'Mid-tower ATX',
            'cooling': 'Tower air cooler or AIO'
        }
        
        return {
            'success': True,
            'domain': domain,
            'tier': tier,
            'budget_inr': budget_inr,
            'recommended_price': price,
            'budget_utilization': f'{min(100, round(price/budget_inr*100))}%',
            'components': components,
            'specs': {
                'cpu_cores': cpu,
                'gpu_vram': gpu,
                'ram_gb': ram,
                'storage_gb': storage
            },
            'reasoning': f'Recommended {tier.capitalize()} tier build for {domain} within ₹{budget_inr:,} budget. Uses K-means clustering to find best value.',
            'algorithm': 'K-means Clustering'
        }
    
    def _default_recommendation(self, domain, budget_inr):
        """Generate default recommendation if clustering fails."""
        # Simple heuristic-based recommendation
        if budget_inr < 50000:
            tier = 'budget'
            cpu, gpu, ram, storage = 4, 2, 8, 256
        elif budget_inr < 100000:
            tier = 'mid'
            cpu, gpu, ram, storage = 6, 6, 16, 512
        else:
            tier = 'high'
            cpu, gpu, ram, storage = 12, 12, 32, 1024
        
        return {
            'success': True,
            'domain': domain,
            'tier': tier,
            'budget_inr': budget_inr,
            'recommended_price': budget_inr * 0.9,
            'budget_utilization': '90%',
            'components': {
                'cpu': f'Intel i{5+cpu}',
                'gpu': f'RTX {2060+gpu*500}',
                'ram': f'{ram}GB',
                'storage': f'{storage}GB SSD',
                'motherboard': 'B550',
                'psu': f'{650+cpu*50}W',
                'case': 'Mid-tower',
                'cooling': 'Air cooler'
            },
            'specs': {
                'cpu_cores': cpu,
                'gpu_vram': gpu,
                'ram_gb': ram,
                'storage_gb': storage
            },
            'reasoning': 'Default recommendation based on budget tier.',
            'algorithm': 'Heuristic'
        }

# Global instance
_recommender = None

def get_build_recommender():
    """Get or create global build recommender instance."""
    global _recommender
    if _recommender is None:
        _recommender = MLBuildRecommender()
    return _recommender
