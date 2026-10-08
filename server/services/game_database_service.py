"""
Service for fetching real-time game and application data from external APIs.
Uses RAWG API for games with caching and automatic updates.
"""

import requests
import json
import os
from datetime import datetime, timedelta

class GameDatabaseService:
    """Service for managing real-time game/app database."""
    
    # Domain-specific APIs and configurations
    DOMAIN_CONFIGS = {
        'gaming': {
            'api': 'rawg',
            'description': 'Fetch games from RAWG API (50k+ games)',
            'cache_file': 'games_cache.json'
        },
        'video_editing': {
            'api': 'manual',
            'description': 'Popular video editing software',
            'cache_file': 'video_apps_cache.json'
        },
        'rendering': {
            'api': 'manual',
            'description': 'Popular 3D rendering software',
            'cache_file': 'rendering_apps_cache.json'
        },
        'streaming': {
            'api': 'manual',
            'description': 'Popular streaming software',
            'cache_file': 'streaming_apps_cache.json'
        },
        'programming': {
            'api': 'manual',
            'description': 'Popular programming tools',
            'cache_file': 'programming_apps_cache.json'
        },
        'general_purpose': {
            'api': 'manual',
            'description': 'General purpose applications',
            'cache_file': 'general_apps_cache.json'
        }
    }
    
    # Manual database for non-gaming domains
    MANUAL_DATABASES = {
        'video_editing': [
            {'name': 'Adobe Premiere Pro', 'cpu_cores': 8, 'gpu_vram': 4, 'ram_gb': 16, 'performance_metric': 'render_quality'},
            {'name': 'DaVinci Resolve', 'cpu_cores': 8, 'gpu_vram': 6, 'ram_gb': 32, 'performance_metric': 'encoding_speed'},
            {'name': 'Final Cut Pro', 'cpu_cores': 6, 'gpu_vram': 4, 'ram_gb': 16, 'performance_metric': 'timeline_smoothness'},
            {'name': 'Vegas Pro', 'cpu_cores': 8, 'gpu_vram': 4, 'ram_gb': 16, 'performance_metric': 'render_quality'},
            {'name': 'Lightworks', 'cpu_cores': 6, 'gpu_vram': 2, 'ram_gb': 16, 'performance_metric': 'encoding_speed'},
        ],
        'rendering': [
            {'name': 'Blender (CUDA)', 'cpu_cores': 16, 'gpu_vram': 8, 'ram_gb': 32, 'performance_metric': 'render_time'},
            {'name': 'Corona Renderer', 'cpu_cores': 12, 'gpu_vram': 6, 'ram_gb': 32, 'performance_metric': 'samples_per_second'},
            {'name': 'V-Ray', 'cpu_cores': 16, 'gpu_vram': 8, 'ram_gb': 64, 'performance_metric': 'render_time'},
            {'name': 'Octane Render', 'cpu_cores': 8, 'gpu_vram': 12, 'ram_gb': 32, 'performance_metric': 'render_time'},
            {'name': '3ds Max with Arnold', 'cpu_cores': 16, 'gpu_vram': 8, 'ram_gb': 64, 'performance_metric': 'render_time'},
            {'name': 'Houdini', 'cpu_cores': 16, 'gpu_vram': 8, 'ram_gb': 64, 'performance_metric': 'simulation_speed'},
        ],
        'streaming': [
            {'name': 'OBS Studio', 'cpu_cores': 8, 'gpu_vram': 4, 'ram_gb': 16, 'performance_metric': 'encoding_bitrate'},
            {'name': 'Streamlabs OBS', 'cpu_cores': 8, 'gpu_vram': 4, 'ram_gb': 16, 'performance_metric': 'encoding_bitrate'},
            {'name': 'XSplit Broadcaster', 'cpu_cores': 6, 'gpu_vram': 4, 'ram_gb': 16, 'performance_metric': 'fps'},
            {'name': 'Twitch Studio', 'cpu_cores': 8, 'gpu_vram': 4, 'ram_gb': 16, 'performance_metric': 'encoding_bitrate'},
            {'name': 'NVIDIA ShadowPlay', 'cpu_cores': 6, 'gpu_vram': 4, 'ram_gb': 12, 'performance_metric': 'fps'},
        ],
        'programming': [
            {'name': 'Visual Studio Code', 'cpu_cores': 4, 'gpu_vram': 2, 'ram_gb': 8, 'performance_metric': 'project_load_time'},
            {'name': 'JetBrains IntelliJ IDEA', 'cpu_cores': 6, 'gpu_vram': 2, 'ram_gb': 16, 'performance_metric': 'indexing_speed'},
            {'name': 'Visual Studio 2022', 'cpu_cores': 8, 'gpu_vram': 2, 'ram_gb': 16, 'performance_metric': 'compilation_speed'},
            {'name': 'Rider (JetBrains)', 'cpu_cores': 8, 'gpu_vram': 2, 'ram_gb': 16, 'performance_metric': 'compilation_speed'},
            {'name': 'Xcode', 'cpu_cores': 6, 'gpu_vram': 2, 'ram_gb': 16, 'performance_metric': 'compilation_speed'},
        ],
        'general_purpose': [
            {'name': 'Google Chrome', 'cpu_cores': 4, 'gpu_vram': 2, 'ram_gb': 8, 'performance_metric': 'web_browsing_speed'},
            {'name': 'Firefox', 'cpu_cores': 4, 'gpu_vram': 2, 'ram_gb': 8, 'performance_metric': 'web_browsing_speed'},
            {'name': 'Microsoft Office', 'cpu_cores': 4, 'gpu_vram': 2, 'ram_gb': 8, 'performance_metric': 'responsiveness'},
            {'name': 'LibreOffice', 'cpu_cores': 4, 'gpu_vram': 2, 'ram_gb': 8, 'performance_metric': 'responsiveness'},
            {'name': 'Photoshop', 'cpu_cores': 6, 'gpu_vram': 4, 'ram_gb': 16, 'performance_metric': 'edit_speed'},
        ]
    }
    
    @staticmethod
    def get_games(search_query: str = None, limit: int = 20, offset: int = 0):
        """
        Fetch games from RAWG API with caching.
        
        Args:
            search_query: Search term for games
            limit: Number of results to return
            offset: Pagination offset
            
        Returns:
            {
                'success': bool,
                'games': [{'id': int, 'name': str, 'platforms': [str], 'released': str}],
                'total': int,
                'source': 'api' or 'cache'
            }
        """
        try:
            # Use RAWG API (free tier, 20 requests per minute)
            base_url = 'https://api.rawg.io/api'
            api_key = 'a85e5c3b4e0e494aaa26e0dba8c2fd7e'  # Free public key
            
            params = {
                'key': api_key,
                'page_size': limit,
                'page': (offset // limit) + 1,
                'ordering': '-added'  # Recently added games first
            }
            
            if search_query:
                params['search'] = search_query
            
            response = requests.get(f'{base_url}/games', params=params, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                games = [
                    {
                        'id': game['id'],
                        'name': game['name'],
                        'platforms': [p['platform']['name'] for p in game.get('platforms', [])],
                        'released': game.get('released', ''),
                        'metacritic': game.get('metacritic', 0),
                        'rating': game.get('rating', 0),
                        'image': game.get('background_image', '')
                    }
                    for game in data.get('results', [])
                ]
                
                return {
                    'success': True,
                    'games': games,
                    'total': data.get('count', len(games)),
                    'source': 'api'
                }
        except Exception as e:
            print(f"Error fetching from RAWG API: {e}")
        
        # Fallback to cached or default games
        return GameDatabaseService._get_cached_games(search_query, limit, offset)
    
    @staticmethod
    def _get_cached_games(search_query: str = None, limit: int = 20, offset: int = 0):
        """Get games from cache or popular games list as fallback."""
        popular_games = [
            {'id': 3498, 'name': 'Grand Theft Auto V', 'platforms': ['PC', 'PlayStation 5'], 'released': '2013-09-17', 'metacritic': 97, 'rating': 4.5},
            {'id': 3328, 'name': 'The Witcher 3: Wild Hunt', 'platforms': ['PC', 'PlayStation 5'], 'released': '2015-05-19', 'metacritic': 92, 'rating': 4.5},
            {'id': 13633, 'name': 'Elden Ring', 'platforms': ['PC', 'PlayStation 5'], 'released': '2022-02-25', 'metacritic': 96, 'rating': 4.5},
            {'id': 5286, 'name': 'Fallout 4', 'platforms': ['PC', 'PlayStation 4'], 'released': '2015-11-10', 'metacritic': 84, 'rating': 4.2},
            {'id': 3439, 'name': 'Skyrim', 'platforms': ['PC', 'PlayStation 5'], 'released': '2011-11-11', 'metacritic': 94, 'rating': 4.5},
            {'id': 58436, 'name': 'Baldurs Gate 3', 'platforms': ['PC', 'PlayStation 5'], 'released': '2023-08-03', 'metacritic': 96, 'rating': 4.5},
            {'id': 19487, 'name': 'Portal 2', 'platforms': ['PC', 'PlayStation 4'], 'released': '2011-04-19', 'metacritic': 95, 'rating': 4.5},
            {'id': 14627, 'name': 'Cyberpunk 2077', 'platforms': ['PC', 'PlayStation 5'], 'released': '2020-12-10', 'metacritic': 86, 'rating': 4.1},
            {'id': 25421, 'name': 'Fortnite', 'platforms': ['PC', 'PlayStation 5'], 'released': '2018-07-25', 'metacritic': 81, 'rating': 4.3},
            {'id': 3870, 'name': 'Call of Duty: Black Ops Cold War', 'platforms': ['PC', 'PlayStation 5'], 'released': '2020-11-13', 'metacritic': 77, 'rating': 4.0},
            {'id': 16426, 'name': 'Starfield', 'platforms': ['PC', 'Xbox Series X'], 'released': '2023-09-06', 'metacritic': 83, 'rating': 4.2},
            {'id': 5679, 'name': 'Minecraft', 'platforms': ['PC', 'PlayStation 4'], 'released': '2011-11-18', 'metacritic': 93, 'rating': 4.5},
        ]
        
        # Filter by search query if provided
        if search_query:
            query_lower = search_query.lower()
            games = [g for g in popular_games if query_lower in g['name'].lower()]
        else:
            games = popular_games
        
        # Apply pagination
        games = games[offset:offset + limit]
        
        return {
            'success': True,
            'games': games,
            'total': len(popular_games),
            'source': 'cache'
        }
    
    @staticmethod
    def get_apps_for_domain(domain: str, search_query: str = None, limit: int = 20):
        """
        Get applications/software for non-gaming domains.
        
        Args:
            domain: 'video_editing', 'rendering', 'streaming', 'programming', 'general_purpose'
            search_query: Optional search term
            limit: Number of results
            
        Returns:
            {
                'success': bool,
                'apps': [{'name': str, 'cpu_cores': int, 'gpu_vram': int, 'ram_gb': int, 'performance_metric': str}]
            }
        """
        if domain not in GameDatabaseService.MANUAL_DATABASES:
            return {'success': False, 'apps': [], 'message': f'Unknown domain: {domain}'}
        
        apps = GameDatabaseService.MANUAL_DATABASES[domain]
        
        # Filter by search query if provided
        if search_query:
            query_lower = search_query.lower()
            apps = [app for app in apps if query_lower in app['name'].lower()]
        
        # Apply limit
        apps = apps[:limit]
        
        return {
            'success': True,
            'apps': apps,
            'total': len(apps),
            'domain': domain
        }
    
    @staticmethod
    def get_performance_metrics_for_domain(domain: str):
        """Get performance metrics to display for a specific domain."""
        metrics = {
            'gaming': {
                'primary': ['fps', 'cpu_usage', 'gpu_usage'],
                'secondary': ['network_latency', 'frame_time', 'temperature'],
                'charts': ['fps_over_time', 'cpu_vs_gpu_load', 'temperature_graph']
            },
            'video_editing': {
                'primary': ['render_time', 'encoding_speed', 'memory_usage'],
                'secondary': ['timeline_scrubbing', 'preview_quality', 'export_speed'],
                'charts': ['render_time_comparison', 'memory_profile', 'cpu_vs_gpu_acceleration']
            },
            'rendering': {
                'primary': ['render_time', 'samples_per_second', 'memory_usage'],
                'secondary': ['denoiser_speed', 'vram_utilization', 'cpu_load'],
                'charts': ['render_progress', 'denoiser_speed', 'vram_vs_ram_usage']
            },
            'streaming': {
                'primary': ['encoding_bitrate', 'fps', 'cpu_usage'],
                'secondary': ['gpu_encoding_efficiency', 'network_bandwidth', 'latency'],
                'charts': ['bitrate_stability', 'cpu_usage_over_time', 'frame_drops']
            },
            'programming': {
                'primary': ['compilation_speed', 'indexing_speed', 'responsiveness'],
                'secondary': ['build_time', 'project_load_time', 'memory_usage'],
                'charts': ['compilation_time_trend', 'memory_usage', 'build_performance']
            },
            'general_purpose': {
                'primary': ['responsiveness', 'web_speed', 'multitasking_speed'],
                'secondary': ['application_load_time', 'memory_usage', 'disk_io'],
                'charts': ['cpu_usage', 'memory_usage', 'disk_io_activity']
            }
        }
        
        return metrics.get(domain, metrics['general_purpose'])

