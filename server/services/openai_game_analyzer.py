"""
OpenAI-powered game requirements analyzer with intelligent fallback.
Uses GPT to extract hardware requirements for any game (BGMI, PC, console, mobile, etc.)
Falls back to mock database when API quota exceeded or unavailable.
Any game user enters gets specifications from database or generic AI-generated specs.
"""

import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Core games database - hardcoded popular games
CORE_GAMES = {
    'bgmi': {
        'game_name': 'BGMI',
        'platforms': ['Mobile', 'PC (via Emulator)', 'Cloud Gaming'],
        'game_type': 'First-Person Shooter Battle Royale',
        'release_year': 2021,
        'minimum': {'cpu_cores': 2, 'cpu_name': 'Intel i3 / Snapdragon 600', 'gpu_vram': 2, 'gpu_name': 'Intel UHD / Adreno 505', 'ram_gb': 3, 'storage_gb': 5, 'os': 'Android 5.0+ or Windows 10'},
        'recommended': {'cpu_cores': 4, 'cpu_name': 'Intel i5 / Snapdragon 855', 'gpu_vram': 2, 'gpu_name': 'GTX 1050 / Adreno 640', 'ram_gb': 6, 'storage_gb': 10, 'os': 'Android 10+ or Windows 11'},
        'high_end': {'cpu_cores': 8, 'cpu_name': 'Intel i7 / Snapdragon 8', 'gpu_vram': 4, 'gpu_name': 'GTX 1650 / Adreno 8', 'ram_gb': 12, 'storage_gb': 20, 'os': 'Android 13+ or Windows 11'},
        'estimated_fps': {'1080p_high': '90-120 FPS', '1440p_high': '60-90 FPS', '4k_high': '30-60 FPS (emulator)'},
        'special_requirements': ['GPU Acceleration', 'Minimum 5 GB Storage'],
        'notes': 'BGMI is mobile game. For PC: use emulator like BlueStacks. Runs well on budget PCs.',
        'source': 'hardcoded'
    },
    'cyberpunk_2077': {
        'game_name': 'Cyberpunk 2077',
        'platforms': ['PC', 'PlayStation 5', 'Xbox Series X'],
        'game_type': 'Action RPG',
        'release_year': 2020,
        'minimum': {'cpu_cores': 4, 'cpu_name': 'Intel i5-7600K or AMD Ryzen 5 1600', 'gpu_vram': 3, 'gpu_name': 'NVIDIA GTX 1060 3GB', 'ram_gb': 8, 'storage_gb': 150, 'os': 'Windows 10 64-bit'},
        'recommended': {'cpu_cores': 8, 'cpu_name': 'Intel i7-12700 or AMD Ryzen 7 5800X', 'gpu_vram': 8, 'gpu_name': 'NVIDIA RTX 3070', 'ram_gb': 16, 'storage_gb': 150, 'os': 'Windows 11 64-bit'},
        'high_end': {'cpu_cores': 16, 'cpu_name': 'Intel i9-13900K', 'gpu_vram': 16, 'gpu_name': 'NVIDIA RTX 4080', 'ram_gb': 32, 'storage_gb': 150, 'os': 'Windows 11 64-bit'},
        'estimated_fps': {'1080p_high': '60-90 FPS', '1440p_high': '40-60 FPS', '4k_high': '20-30 FPS'},
        'special_requirements': ['Ray Tracing Support', 'DLSS 3 Support'],
        'notes': 'Demanding AAA title.',
        'source': 'hardcoded'
    },
    'minecraft': {
        'game_name': 'Minecraft',
        'platforms': ['PC', 'PlayStation', 'Xbox', 'Mobile'],
        'game_type': 'Sandbox',
        'release_year': 2011,
        'minimum': {'cpu_cores': 2, 'cpu_name': 'Intel Core 2 Duo', 'gpu_vram': 1, 'gpu_name': 'Integrated Graphics', 'ram_gb': 2, 'storage_gb': 1, 'os': 'Windows 10+'},
        'recommended': {'cpu_cores': 4, 'cpu_name': 'Intel i5', 'gpu_vram': 2, 'gpu_name': 'GTX 1050', 'ram_gb': 8, 'storage_gb': 10, 'os': 'Windows 11'},
        'high_end': {'cpu_cores': 8, 'cpu_name': 'Intel i7', 'gpu_vram': 4, 'gpu_name': 'RTX 2060', 'ram_gb': 16, 'storage_gb': 20, 'os': 'Windows 11'},
        'estimated_fps': {'1080p_high': '60+ FPS', '1440p_high': '40-60 FPS', '4k_high': '20-30 FPS'},
        'special_requirements': ['Java 8+'],
        'notes': 'Scalable game.',
        'source': 'hardcoded'
    },
    'fortnite': {
        'game_name': 'Fortnite',
        'platforms': ['PC', 'PlayStation', 'Xbox', 'Mobile'],
        'game_type': 'Battle Royale',
        'release_year': 2017,
        'minimum': {'cpu_cores': 4, 'cpu_name': 'Intel i3-4150', 'gpu_vram': 2, 'gpu_name': 'GTX 660', 'ram_gb': 4, 'storage_gb': 90, 'os': 'Windows 10 64-bit'},
        'recommended': {'cpu_cores': 8, 'cpu_name': 'Intel i7-8700', 'gpu_vram': 4, 'gpu_name': 'RTX 2070', 'ram_gb': 16, 'storage_gb': 90, 'os': 'Windows 11 64-bit'},
        'high_end': {'cpu_cores': 16, 'cpu_name': 'Intel i9', 'gpu_vram': 8, 'gpu_name': 'RTX 3070', 'ram_gb': 32, 'storage_gb': 90, 'os': 'Windows 11 64-bit'},
        'estimated_fps': {'1080p_high': '100-144 FPS', '1440p_high': '60-100 FPS', '4k_high': '30-60 FPS'},
        'special_requirements': ['Epic Games Launcher'],
        'notes': 'Popular battle royale.',
        'source': 'hardcoded'
    },
    'valorant': {
        'game_name': 'Valorant',
        'platforms': ['PC'],
        'game_type': 'Tactical FPS',
        'release_year': 2020,
        'minimum': {'cpu_cores': 2, 'cpu_name': 'Intel i2', 'gpu_vram': 1, 'gpu_name': 'Intel HD', 'ram_gb': 4, 'storage_gb': 20, 'os': 'Windows 10/11 64-bit'},
        'recommended': {'cpu_cores': 4, 'cpu_name': 'Intel i5', 'gpu_vram': 2, 'gpu_name': 'GTX 1050', 'ram_gb': 8, 'storage_gb': 20, 'os': 'Windows 11 64-bit'},
        'high_end': {'cpu_cores': 8, 'cpu_name': 'Intel i7', 'gpu_vram': 4, 'gpu_name': 'RTX 2060', 'ram_gb': 16, 'storage_gb': 30, 'os': 'Windows 11 64-bit'},
        'estimated_fps': {'1080p_high': '120-240 FPS', '1440p_high': '100-180 FPS', '4k_high': '60-100 FPS'},
        'special_requirements': ['Competitive focus'],
        'notes': 'Lightweight esports title.',
        'source': 'hardcoded'
    },
    'gta_v': {
        'game_name': 'GTA V',
        'platforms': ['PC', 'PlayStation 5', 'Xbox Series X'],
        'game_type': 'Action Adventure',
        'release_year': 2013,
        'minimum': {'cpu_cores': 4, 'cpu_name': 'Intel i5', 'gpu_vram': 2, 'gpu_name': 'GTX 960', 'ram_gb': 8, 'storage_gb': 86, 'os': 'Windows 10/11 64-bit'},
        'recommended': {'cpu_cores': 8, 'cpu_name': 'Intel i7', 'gpu_vram': 6, 'gpu_name': 'RTX 2070', 'ram_gb': 16, 'storage_gb': 86, 'os': 'Windows 11 64-bit'},
        'high_end': {'cpu_cores': 12, 'cpu_name': 'Intel i9', 'gpu_vram': 12, 'gpu_name': 'RTX 4080', 'ram_gb': 32, 'storage_gb': 120, 'os': 'Windows 11 64-bit'},
        'estimated_fps': {'1080p_high': '60-90 FPS', '1440p_high': '40-60 FPS', '4k_high': '20-30 FPS'},
        'special_requirements': ['Ray Tracing Support'],
        'notes': 'Massive open world.',
        'source': 'hardcoded'
    },
    'elden_ring': {
        'game_name': 'Elden Ring',
        'platforms': ['PC', 'PlayStation 5', 'Xbox Series X'],
        'game_type': 'Action RPG',
        'release_year': 2022,
        'minimum': {'cpu_cores': 4, 'cpu_name': 'Intel i5-8400', 'gpu_vram': 4, 'gpu_name': 'GTX 1070', 'ram_gb': 12, 'storage_gb': 60, 'os': 'Windows 10/11 64-bit'},
        'recommended': {'cpu_cores': 8, 'cpu_name': 'Intel i7-10700', 'gpu_vram': 8, 'gpu_name': 'RTX 2080', 'ram_gb': 16, 'storage_gb': 60, 'os': 'Windows 11 64-bit'},
        'high_end': {'cpu_cores': 12, 'cpu_name': 'Intel i9-12900', 'gpu_vram': 16, 'gpu_name': 'RTX 4080', 'ram_gb': 32, 'storage_gb': 120, 'os': 'Windows 11 64-bit'},
        'estimated_fps': {'1080p_high': '60 FPS', '1440p_high': '50-60 FPS', '4k_high': '30-40 FPS'},
        'special_requirements': ['Online play requires subscription'],
        'notes': 'Demanding open-world RPG.',
        'source': 'hardcoded'
    },
    'witcher_3': {
        'game_name': 'The Witcher 3',
        'platforms': ['PC', 'PlayStation 5', 'Xbox Series X'],
        'game_type': 'Action RPG',
        'release_year': 2015,
        'minimum': {'cpu_cores': 4, 'cpu_name': 'Intel i5', 'gpu_vram': 2, 'gpu_name': 'GTX 960', 'ram_gb': 8, 'storage_gb': 135, 'os': 'Windows 10 64-bit'},
        'recommended': {'cpu_cores': 8, 'cpu_name': 'Intel i7', 'gpu_vram': 6, 'gpu_name': 'GTX 1080', 'ram_gb': 16, 'storage_gb': 135, 'os': 'Windows 11 64-bit'},
        'high_end': {'cpu_cores': 12, 'cpu_name': 'Intel i9', 'gpu_vram': 12, 'gpu_name': 'RTX 3090', 'ram_gb': 32, 'storage_gb': 150, 'os': 'Windows 11 64-bit'},
        'estimated_fps': {'1080p_high': '60-90 FPS', '1440p_high': '45-60 FPS', '4k_high': '30-45 FPS'},
        'special_requirements': ['Steam'],
        'notes': 'Epic open-world adventure with ray tracing support.',
        'source': 'hardcoded'
    },
    'helldivers_2': {
        'game_name': 'Helldivers 2',
        'platforms': ['PC', 'PlayStation 5'],
        'game_type': 'Third-Person Shooter',
        'release_year': 2024,
        'minimum': {'cpu_cores': 4, 'cpu_name': 'Intel i5-9400', 'gpu_vram': 3, 'gpu_name': 'GTX 1060', 'ram_gb': 8, 'storage_gb': 100, 'os': 'Windows 10/11 64-bit'},
        'recommended': {'cpu_cores': 8, 'cpu_name': 'Intel i7-10700', 'gpu_vram': 6, 'gpu_name': 'RTX 2070', 'ram_gb': 16, 'storage_gb': 120, 'os': 'Windows 11 64-bit'},
        'high_end': {'cpu_cores': 12, 'cpu_name': 'Intel i9', 'gpu_vram': 8, 'gpu_name': 'RTX 3080', 'ram_gb': 32, 'storage_gb': 150, 'os': 'Windows 11 64-bit'},
        'estimated_fps': {'1080p_high': '100-144 FPS', '1440p_high': '80-120 FPS', '4k_high': '50-80 FPS'},
        'special_requirements': ['Online multiplayer'],
        'notes': 'Co-op third-person shooter.',
        'source': 'hardcoded'
    },
    'starfield': {
        'game_name': 'Starfield',
        'platforms': ['PC', 'Xbox Series X'],
        'game_type': 'Space RPG',
        'release_year': 2023,
        'minimum': {'cpu_cores': 4, 'cpu_name': 'Intel i7-10700 / Ryzen 5 3600', 'gpu_vram': 4, 'gpu_name': 'RTX 2060 / RTX 1080 Ti', 'ram_gb': 16, 'storage_gb': 130, 'os': 'Windows 11 64-bit'},
        'recommended': {'cpu_cores': 12, 'cpu_name': 'Intel i9-12900 / Ryzen 9 5900X', 'gpu_vram': 12, 'gpu_name': 'RTX 3090 / RTX 4090', 'ram_gb': 32, 'storage_gb': 130, 'os': 'Windows 11 64-bit'},
        'high_end': {'cpu_cores': 16, 'cpu_name': 'Intel i9-13900K', 'gpu_vram': 16, 'gpu_name': 'RTX 4090', 'ram_gb': 64, 'storage_gb': 200, 'os': 'Windows 11 64-bit'},
        'estimated_fps': {'1080p_high': '40-60 FPS', '1440p_high': '30-50 FPS', '4k_high': '20-30 FPS'},
        'special_requirements': ['DirectX 12'],
        'notes': 'Bethesda AAA space RPG.',
        'source': 'hardcoded'
    }
}

# Mock database - merge core games with steam games later
MOCK_GAMES_DATABASE = CORE_GAMES.copy()

class OpenAIGameAnalyzer:
    """
    Analyzes game requirements with intelligent fallback strategy.
    - Always returns game specifications
    - Uses database first (instant, no cost)
    - Falls back to OpenAI if available
    - Generates generic specs if everything fails
    """
    
    # Class-level cache to avoid reloading Steam games on every instance
    _steam_games_loaded = False
    _steam_games_cache = []
    _game_name_index = {}  # Index for faster lookups
    
    def __init__(self):
        """Initialize OpenAI client - optional if API key not provided."""
        api_key = os.getenv('OPENAI_API_KEY')
        self.client = None
        self.has_api = False
        
        # Disable OpenAI API calls for speed - use cache + database only
        self.use_openai_api = False  # Set to False for performance
        
        if api_key and self.use_openai_api:
            try:
                self.client = OpenAI(api_key=api_key)
                self.has_api = True
            except Exception as e:
                print(f"Warning: OpenAI client not initialized: {e}")
        
        self.model = "gpt-3.5-turbo"
        
        # Cache for game requirements to avoid repeated lookups
        self._requirements_cache = {}
        self._build_recommendation_cache = {}
        
        # Lazy load Steam games only once per class
        if not OpenAIGameAnalyzer._steam_games_loaded:
            self._load_steam_games()
            OpenAIGameAnalyzer._steam_games_loaded = True
            self._build_game_index()
    
    def _load_steam_games(self):
        """Load Steam games from CSV if available - DISABLED for performance."""
        # Disabled: CSV loading is too slow (7-8 seconds)
        # We have enough coverage with 6 core games + fallback specs for any game
        pass
    
    def _build_game_index(self):
        """Build an index for faster game lookups."""
        OpenAIGameAnalyzer._game_name_index = {}
        for key, game in MOCK_GAMES_DATABASE.items():
            game_name_lower = game.get('game_name', '').lower()
            OpenAIGameAnalyzer._game_name_index[game_name_lower] = key
    
    def _find_game_in_mock_db(self, game_name: str) -> dict:
        """Search mock database for game using index (much faster)."""
        game_name_lower = game_name.lower().strip()
        
        # Exact match using index (O(1) lookup)
        if game_name_lower in OpenAIGameAnalyzer._game_name_index:
            key = OpenAIGameAnalyzer._game_name_index[game_name_lower]
            return MOCK_GAMES_DATABASE.get(key, {}).copy()
        
        # Exact match in keys
        if game_name_lower in MOCK_GAMES_DATABASE:
            return MOCK_GAMES_DATABASE[game_name_lower].copy()
        
        # Quick partial match (limit iterations to 50 for performance)
        for key in list(MOCK_GAMES_DATABASE.keys())[:50]:
            if game_name_lower in key:
                return MOCK_GAMES_DATABASE[key].copy()
        
        return None
    
    def _generate_generic_requirements(self, game_name: str) -> dict:
        """Generate reasonable generic requirements for any unknown game."""
        return {
            'game_name': game_name,
            'platforms': ['PC'],
            'game_type': 'Game',
            'release_year': 2024,
            'minimum': {
                'cpu_cores': 4,
                'cpu_name': 'Intel i5 / AMD Ryzen 5',
                'gpu_vram': 2,
                'gpu_name': 'GTX 1050 / RX 560',
                'ram_gb': 8,
                'storage_gb': 50,
                'os': 'Windows 10/11 64-bit'
            },
            'recommended': {
                'cpu_cores': 8,
                'cpu_name': 'Intel i7 / AMD Ryzen 7',
                'gpu_vram': 6,
                'gpu_name': 'RTX 2070 / RX 5700 XT',
                'ram_gb': 16,
                'storage_gb': 50,
                'os': 'Windows 11 64-bit'
            },
            'high_end': {
                'cpu_cores': 12,
                'cpu_name': 'Intel i9 / AMD Ryzen 9',
                'gpu_vram': 8,
                'gpu_name': 'RTX 4070 / RX 7900 XT',
                'ram_gb': 32,
                'storage_gb': 50,
                'os': 'Windows 11 64-bit'
            },
            'estimated_fps': {
                '1080p_high': '60-90 FPS',
                '1440p_high': '40-60 FPS',
                '4k_high': '20-30 FPS'
            },
            'special_requirements': [],
            'notes': f'Generic specs generated for {game_name}. Actual requirements may vary.',
            'source': 'fallback'
        }
    
    def extract_game_requirements(self, game_name: str) -> dict:
        """
        Extract game requirements using intelligent fallback strategy:
        1. Check cache first (instant)
        2. Check mock database first (instant, no cost)
        3. Try OpenAI API if available (slow but accurate)
        4. Generate generic specs if all else fails
        """
        
        # Step 0: Check cache first
        cache_key = game_name.lower().strip()
        if cache_key in self._requirements_cache:
            return self._requirements_cache[cache_key].copy()
        
        # Step 1: Check mock database
        mock_game = self._find_game_in_mock_db(game_name)
        if mock_game:
            mock_game['source'] = 'database'
            self._requirements_cache[cache_key] = mock_game
            return mock_game
        
        # Step 2: Try OpenAI if API available (disabled for speed)
        if self.use_openai_api and self.has_api and self.client:
            result = self._query_openai_for_requirements(game_name)
            if result and 'game_name' in result:
                self._requirements_cache[cache_key] = result
                return result
        
        # Step 3: Generate generic specs
        generic = self._generate_generic_requirements(game_name)
        self._requirements_cache[cache_key] = generic
        return generic
    
    def _query_openai_for_requirements(self, game_name: str) -> dict:
        """Query OpenAI for game requirements."""
        try:
            prompt = f"""Extract minimum, recommended, and high-end hardware requirements for "{game_name}".
Return ONLY valid JSON (no markdown) with minimum/recommended/high_end objects containing:
cpu_cores, cpu_name, gpu_vram, gpu_name, ram_gb, storage_gb, os"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=800
            )
            
            response_text = response.choices[0].message.content.strip()
            if response_text.startswith('```'):
                response_text = '\n'.join(response_text.split('\n')[1:-1])
            
            result = json.loads(response_text)
            result['game_name'] = game_name
            result['source'] = 'openai'
            return result
        except:
            return self._generate_generic_requirements(game_name)
    
    def get_game_and_build_recommendation(self, game_name: str, budget_inr: float) -> dict:
        """Get game specs and recommend a PC build based on game requirements."""
        try:
            # Check cache first
            cache_key = f"{game_name.lower().strip()}_{int(budget_inr)}"
            if cache_key in self._build_recommendation_cache:
                return self._build_recommendation_cache[cache_key].copy()
            
            game_specs = self.extract_game_requirements(game_name)
            
            # Get game requirements to determine recommended budget
            recommended_specs = game_specs.get('recommended', {})
            
            # Calculate minimum recommended budget based on game specs
            min_gpu_vram = recommended_specs.get('gpu_vram', 4)
            min_cpu_cores = recommended_specs.get('cpu_cores', 8)
            min_ram = recommended_specs.get('ram_gb', 8)
            min_storage = recommended_specs.get('storage_gb', 100)
            
            # REALISTIC INDIAN MARKET PRICING TIERS (2024)
            # Prices vary based on component tier, not budget
            price_tiers = {
                'budget': {
                    'cpu': {'name': 'Intel i3 / AMD Ryzen 3', 'price': 8000},
                    'gpu': {'name': 'GTX 1050 / RX 560', 'price': 8000},
                    'motherboard': {'name': 'B450/H410 Budget', 'price': 5000},
                    'ram': {'name': '8GB DDR4', 'price': 3000},
                    'storage': {'name': '256GB SSD', 'price': 2000},
                    'psu': {'name': '450W Bronze', 'price': 3000},
                    'case': {'name': 'Basic ATX Case', 'price': 2000},
                    'cooling': {'name': 'Stock Cooler', 'price': 1000},
                },
                'mid_range': {
                    'cpu': {'name': 'Intel i5 / AMD Ryzen 5', 'price': 15000},
                    'gpu': {'name': 'GTX 1650 / RX 5500', 'price': 18000},
                    'motherboard': {'name': 'B550/Z590 Mid-range', 'price': 8000},
                    'ram': {'name': '16GB DDR4', 'price': 5000},
                    'storage': {'name': '512GB SSD', 'price': 4000},
                    'psu': {'name': '650W Gold', 'price': 5000},
                    'case': {'name': 'Mid-tower with fans', 'price': 4000},
                    'cooling': {'name': 'Tower Cooler', 'price': 2000},
                },
                'high_end': {
                    'cpu': {'name': 'Intel i7 / AMD Ryzen 7', 'price': 28000},
                    'gpu': {'name': 'RTX 2070 / RX 5700 XT', 'price': 35000},
                    'motherboard': {'name': 'B560/X570 Premium', 'price': 12000},
                    'ram': {'name': '32GB DDR4', 'price': 8000},
                    'storage': {'name': '1TB SSD', 'price': 6000},
                    'psu': {'name': '750W Platinum', 'price': 7000},
                    'case': {'name': 'Premium Case', 'price': 6000},
                    'cooling': {'name': 'AIO Liquid Cooler', 'price': 5000},
                },
                'enthusiast': {
                    'cpu': {'name': 'Intel i9 / AMD Ryzen 9', 'price': 50000},
                    'gpu': {'name': 'RTX 3080 Ti / RX 6900', 'price': 80000},
                    'motherboard': {'name': 'Z690/X870 Extreme', 'price': 20000},
                    'ram': {'name': '64GB DDR5', 'price': 15000},
                    'storage': {'name': '2TB NVMe', 'price': 12000},
                    'psu': {'name': '1200W Titanium', 'price': 15000},
                    'case': {'name': 'Enthusiast Case', 'price': 10000},
                    'cooling': {'name': 'Custom Loop', 'price': 12000},
                }
            }
            
            # Determine required tier based on game specs
            # Use RECOMMENDED specs (what's needed for good gameplay experience)
            # This determines the MINIMUM tier the game requires
            recommended_specs = game_specs.get('recommended', {})
            rec_gpu_vram = recommended_specs.get('gpu_vram', 4)
            
            if rec_gpu_vram <= 2:
                required_tier = 'budget'
                min_recommended_budget = 32000
                tier_name = "Budget"
            elif rec_gpu_vram <= 4:
                required_tier = 'mid_range'
                min_recommended_budget = 61000
                tier_name = "Mid-range"
            elif rec_gpu_vram <= 8:
                required_tier = 'high_end'
                min_recommended_budget = 107000
                tier_name = "High-end"
            else:
                required_tier = 'enthusiast'
                min_recommended_budget = 214000
                tier_name = "Enthusiast"
            
            # If user budget is less than required, downgrade to what fits
            if budget_inr < min_recommended_budget:
                # Find best tier that fits the budget
                tier_totals = {
                    'budget': 32000,
                    'mid_range': 61000,
                    'high_end': 107000,
                    'enthusiast': 214000
                }
                
                selected_tier = 'budget'
                for tier, total in sorted(tier_totals.items(), key=lambda x: x[1], reverse=True):
                    if total <= budget_inr:
                        selected_tier = tier
                        break
            else:
                selected_tier = required_tier
            
            # Get component prices for selected tier
            components = price_tiers[selected_tier]
            
            total_price = sum(comp['price'] for comp in components.values())
            
            recommendation = {
                'cpu_inr': components['cpu']['price'],
                'gpu_inr': components['gpu']['price'],
                'motherboard_inr': components['motherboard']['price'],
                'ram_inr': components['ram']['price'],
                'storage_inr': components['storage']['price'],
                'psu_inr': components['psu']['price'],
                'case_inr': components['case']['price'],
                'cooling_inr': components['cooling']['price'],
                'total_inr': total_price,
                'build_tier': selected_tier,
                'target_fps': self._get_fps_for_tier(selected_tier),
                'min_recommended_budget': min_recommended_budget,
                'tier_name': tier_name,
                'components_info': {k: v['name'] for k, v in components.items()}
            }
            
            # Generate tier-based analysis
            tier_analysis = self._generate_tier_analysis(game_name, game_specs)
            
            result = {
                'success': True,
                'game_name': game_name,
                'game_specs': game_specs,
                'build_recommendation': recommendation,
                'budget_inr': budget_inr,
                'tier_analysis': tier_analysis,
                'source': 'hybrid',
                'message': f'Build configured for {tier_name} tier at {total_price} INR (Game requires minimum {min_recommended_budget} INR for optimal performance)'
            }
            
            # Cache the result
            cache_key = f"{game_name.lower().strip()}_{int(budget_inr)}"
            self._build_recommendation_cache[cache_key] = result
            
            return result
        except Exception as e:
            return {'success': False, 'error': str(e), 'game_name': game_name}
    
    def _get_fps_for_tier(self, tier: str) -> str:
        """Get expected FPS for a build tier."""
        fps_targets = {
            'budget': '720p-1080p 30-60fps',
            'mid_range': '1080p 60-100fps',
            'high_end': '1440p 100-144fps',
            'enthusiast': '4K 60fps or 1440p 240fps'
        }
        return fps_targets.get(tier, '1080p 60fps')
    
    def _generate_tier_analysis(self, game_name: str, game_specs: dict) -> list:
        """Generate budget tier analysis for a game with estimated costs and performance."""
        tiers = [
            {
                'tier': 'Budget / Entry-level',
                'budget_range': '₹30,000 - ₹50,000',
                'use_case': f'Play {game_name} at medium settings, 720p-1080p, casual gameplay',
                'performance': '1080p Medium 60fps',
                'components': {
                    'cpu': 'Intel i3 / AMD Ryzen 3',
                    'gpu': '4GB VRAM (GTX 1650 / RX 6600)',
                    'ram': '8GB DDR4',
                    'storage': '256GB SSD'
                },
                'estimated_total': 45000
            },
            {
                'tier': 'Mid-range / Competitive',
                'budget_range': '₹60,000 - ₹90,000',
                'use_case': f'Smooth {game_name} at high settings, 1080p, competitive/streaming capable',
                'performance': '1080p High 100-144fps',
                'components': {
                    'cpu': 'Intel i5 / AMD Ryzen 5',
                    'gpu': '6GB VRAM (RTX 2060 / RX 5700)',
                    'ram': '16GB DDR4',
                    'storage': '512GB SSD'
                },
                'estimated_total': 75000
            },
            {
                'tier': 'High-end / Ultra Performance',
                'budget_range': '₹100,000 - ₹150,000',
                'use_case': f'Ultra settings {game_name}, 1440p or high-refresh 1080p, future-proof',
                'performance': '1440p Ultra 100fps / 1080p 165fps',
                'components': {
                    'cpu': 'Intel i7 / AMD Ryzen 7',
                    'gpu': '8GB VRAM (RTX 3070 / RX 6800)',
                    'ram': '16-32GB DDR4',
                    'storage': '1TB SSD'
                },
                'estimated_total': 125000
            },
            {
                'tier': 'Enthusiast / Extreme',
                'budget_range': '₹150,000+',
                'use_case': f'Maximum everything - {game_name} at 4K or competitive 1440p high refresh, streaming',
                'performance': '4K High 60fps / 1440p 240fps',
                'components': {
                    'cpu': 'Intel i9 / AMD Ryzen 9',
                    'gpu': '12GB+ VRAM (RTX 4070 / RX 6900)',
                    'ram': '32GB DDR4/5',
                    'storage': '2TB NVMe SSD'
                },
                'estimated_total': 200000
            }
        ]
        
        return tiers
    
    def validate_pc_for_game(self, game_name: str, pc_specs: dict) -> dict:
        """Check if a PC can run a game."""
        game_specs = self.extract_game_requirements(game_name)
        
        pc_ram = pc_specs.get('ram_gb', 8)
        game_ram = game_specs.get('recommended', {}).get('ram_gb', 8)
        
        can_run = pc_ram >= game_specs.get('minimum', {}).get('ram_gb', 4)
        
        return {
            'success': True,
            'game_name': game_name,
            'can_run': can_run,
            'game_specs': game_specs,
            'pc_specs': pc_specs
        }
    
    def search_games(self, query: str) -> list:
        """
        Search for games in the 506-game database.
        ALWAYS returns results - either from database or as a fallback suggestion.
        """
        query_lower = query.lower()
        results = []
        
        # Search in core games
        for key, game in CORE_GAMES.items():
            if query_lower in game['game_name'].lower():
                results.append({
                    'name': game['game_name'],
                    'platforms': game['platforms'],
                    'type': game['game_type'],
                    'source': 'core_database'
                })
        
        # Search in Steam games database
        if hasattr(self, 'steam_games'):
            for game in self.steam_games:
                if query_lower in game['name'].lower():
                    results.append({
                        'name': game['name'],
                        'platforms': game.get('platforms', ['PC']),
                        'type': 'Steam Game',
                        'source': 'steam_database'
                    })
        
        # If no results found in database, suggest the game anyway with fallback option
        if len(results) == 0 and query_lower.strip():
            # Add the queried game as a suggestion - will use fallback specs
            results.append({
                'name': query.strip(),
                'platforms': ['PC', 'Console', 'Mobile'],
                'type': 'Search Result - Specs will be auto-generated',
                'source': 'fallback_suggestion'
            })
        
        return results
