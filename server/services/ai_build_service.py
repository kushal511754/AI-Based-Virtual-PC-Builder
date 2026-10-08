"""
AI-powered PC build recommendation service.
Analyzes domain requirements and budget to suggest compatible parts.
Integrates PCBuildAgent for real Indian market pricing in INR.
"""

import hashlib
import json
import re
import time
from server.utils.db import get_db
from server.services.compatibility_engine import CompatibilityEngine
from server.services.pc_build_agent import PCBuildAgent

class AIBuildService:
    """Service for AI-powered PC build recommendations."""
    
    # Cache for build suggestions (domain_game_budget -> result)
    _build_cache = {}
    _cache_timeout = 3600  # 1 hour cache validity
    
    # Domain specifications
    DOMAINS = {
        'gaming': {
            'name': 'Gaming',
            'min_cpu_cores': 6,
            'min_gpu_vram': 4,
            'min_ram_gb': 16,
            'min_storage_gb': 500,
            'min_psu_wattage': 650,
            'priority': 'gpu'  # GPU matters most for gaming
        },
        'video_editing': {
            'name': 'Video Editing',
            'min_cpu_cores': 8,
            'min_gpu_vram': 6,
            'min_ram_gb': 32,
            'min_storage_gb': 2000,
            'min_psu_wattage': 750,
            'priority': 'cpu'  # CPU matters most for video editing
        },
        'programming': {
            'name': 'Programming',
            'min_cpu_cores': 4,
            'min_gpu_vram': 2,
            'min_ram_gb': 16,
            'min_storage_gb': 512,
            'min_psu_wattage': 550,
            'priority': 'cpu'  # CPU for compilation
        },
        'streaming': {
            'name': 'Streaming',
            'min_cpu_cores': 8,
            'min_gpu_vram': 4,
            'min_ram_gb': 24,
            'min_storage_gb': 1000,
            'min_psu_wattage': 750,
            'priority': 'balanced'  # Both CPU and GPU matter
        },
        'rendering': {
            'name': 'Rendering',
            'min_cpu_cores': 16,
            'min_gpu_vram': 8,
            'min_ram_gb': 64,
            'min_storage_gb': 2000,
            'min_psu_wattage': 850,
            'priority': 'gpu'  # GPU for CUDA/rendering
        },
        'general_purpose': {
            'name': 'General Purpose',
            'min_cpu_cores': 4,
            'min_gpu_vram': 2,
            'min_ram_gb': 8,
            'min_storage_gb': 256,
            'min_psu_wattage': 450,
            'priority': 'balanced'
        }
    }

    @staticmethod
    def _assess_catalogue_compatibility(parts):
        """Check what can be established from the recommendation catalogue."""
        def text_for(key):
            part = parts.get(key) or {}
            return f"{part.get('name', '')} {part.get('specs', '')}"

        cpu_text = text_for('cpu').lower()
        board_text = text_for('motherboard').lower()
        ram_text = text_for('ram').lower()
        cooler_text = text_for('cooler').lower()
        psu_text = text_for('psu').lower()
        gpu_text = text_for('gpu').lower()

        cpu_socket = 'AM5' if 'ryzen' in cpu_text and re.search(r'ryzen\s+[789]\s+[789]', cpu_text) else None
        if 'ryzen' in cpu_text and not cpu_socket:
            cpu_socket = 'AM4'
        if re.search(r'\b(i[3579]-?1[234]\d{3}|core\s+i[3579]-?1[234]\d{3})', cpu_text):
            cpu_socket = 'LGA1700'

        board_socket = next((socket for socket in ('AM4', 'AM5', 'LGA1700') if socket.lower() in board_text), None)
        if not board_socket and re.search(r'a520|b450m?|b550', board_text):
            board_socket = 'AM4'
        if not board_socket and re.search(r'b660m?|b760|z690|z790', board_text):
            board_socket = 'LGA1700'

        checks = []
        def add_check(name, status, detail):
            checks.append({'name': name, 'status': status, 'detail': detail})

        if cpu_socket and board_socket:
            match = cpu_socket == board_socket
            add_check('CPU and motherboard socket', 'pass' if match else 'fail',
                      f'{cpu_socket} CPU and {board_socket} motherboard' if match else f'{cpu_socket} CPU does not match {board_socket} motherboard')
        else:
            add_check('CPU and motherboard socket', 'review', 'Socket details are incomplete in the catalogue; check the exact motherboard revision before ordering.')

        ram_match = re.search(r'\bddr\s?([345])\b', ram_text)
        board_ram = re.search(r'\bddr\s?([345])\b', board_text)
        if not board_ram and board_socket == 'AM4':
            board_ram = re.match(r'ddr([345])', 'ddr4')
        if not board_ram and board_socket == 'AM5':
            board_ram = re.match(r'ddr([345])', 'ddr5')
        if ram_match and board_ram:
            ram_type = f'DDR{ram_match.group(1)}'
            board_type = f'DDR{board_ram.group(1)}'
            add_check('Memory and motherboard', 'pass' if ram_type == board_type else 'fail',
                      f'{ram_type} memory with a {board_type} motherboard' if ram_type == board_type else f'{ram_type} memory does not match {board_type} motherboard')
        else:
            add_check('Memory and motherboard', 'review', 'Motherboard memory type is not listed clearly; verify DDR generation and capacity before ordering.')

        psu_watts = re.search(r'(\d{3,4})\s?w', psu_text)
        gpu_watts = re.search(r'~\s?(\d{2,3})\s?w', gpu_text)
        known_gpu_watts = {'rtx 3050': 115, 'rtx 4060': 115, 'rtx 4060 ti': 160, 'rtx 4070': 200, 'rtx 3060': 170, 'gtx 1650': 75}
        if not gpu_watts:
            gpu_watts = next((re.match(r'(\d+)', str(watts)) for model, watts in known_gpu_watts.items() if model in gpu_text), None)
        cpu_watts = 65
        if any(tag in cpu_text for tag in ('13600k', '13700', '13900', '14900')):
            cpu_watts = 181
        elif any(tag in cpu_text for tag in ('5700x', '5800x')):
            cpu_watts = 105
        if psu_watts and gpu_watts:
            required = cpu_watts + int(gpu_watts.group(1)) + 150
            available = int(psu_watts.group(1))
            add_check('Power supply capacity', 'pass' if available >= required else 'fail',
                      f'Estimated {required}W requirement with {available}W PSU (CPU/GPU estimate plus 150W headroom).')
        else:
            add_check('Power supply capacity', 'review', 'Power details are incomplete; verify the PSU wattage against the exact CPU and GPU models.')

        add_check('Graphics card and case clearance', 'review', 'The catalogue has no exact GPU and case clearance measurements; confirm card length against the case before ordering.')
        cooler_socket = next((socket for socket in ('AM4', 'AM5', 'LGA1700') if socket.lower() in cooler_text), None)
        if 'wraith stealth' in cooler_text and cpu_socket == 'AM4':
            add_check('CPU cooler mounting', 'pass', 'The stock AMD Wraith cooler matches the AM4 CPU socket.')
        elif cooler_socket and cpu_socket:
            add_check('CPU cooler mounting', 'pass' if cooler_socket == cpu_socket else 'fail',
                      f'{cooler_socket} cooler mounting with {cpu_socket} CPU socket')
        else:
            add_check('CPU cooler mounting', 'review', 'Cooler mounting socket is not fully specified; confirm the included mounting kit.')

        status = 'incompatible' if any(check['status'] == 'fail' for check in checks) else (
            'review' if any(check['status'] == 'review' for check in checks) else 'compatible')
        return {
            'status': status,
            'compatible': status == 'compatible' if status != 'review' else None,
            'checks': checks,
            'errors': [check['detail'] for check in checks if check['status'] == 'fail'],
            'warnings': [check['detail'] for check in checks if check['status'] == 'review']
        }
    
    @staticmethod
    def get_domains():
        """Get all available domains."""
        return AIBuildService.DOMAINS
    
    @staticmethod
    def analyze_budget(domain, budget):
        """
        Analyze if budget is sufficient for domain.
        Returns: {sufficient: bool, message: str, budget_breakdown: dict}
        """
        domain_specs = AIBuildService.DOMAINS.get(domain)
        if not domain_specs:
            return {'sufficient': False, 'message': 'Invalid domain', 'budget_breakdown': {}}
        
        # Rough budget allocation per domain (in percentage)
        budget_allocation = {
            'gaming': {'cpu': 20, 'gpu': 40, 'motherboard': 10, 'ram': 15, 'storage': 5, 'psu': 5, 'case': 3, 'cooling': 2},
            'video_editing': {'cpu': 35, 'gpu': 25, 'motherboard': 10, 'ram': 20, 'storage': 5, 'psu': 3, 'case': 1, 'cooling': 1},
            'programming': {'cpu': 30, 'gpu': 10, 'motherboard': 10, 'ram': 25, 'storage': 15, 'psu': 5, 'case': 3, 'cooling': 2},
            'streaming': {'cpu': 30, 'gpu': 30, 'motherboard': 10, 'ram': 15, 'storage': 5, 'psu': 5, 'case': 3, 'cooling': 2},
            'rendering': {'cpu': 25, 'gpu': 45, 'motherboard': 10, 'ram': 12, 'storage': 3, 'psu': 3, 'case': 1, 'cooling': 1},
            'general_purpose': {'cpu': 25, 'gpu': 15, 'motherboard': 12, 'ram': 20, 'storage': 15, 'psu': 8, 'case': 3, 'cooling': 2}
        }
        
        allocation = budget_allocation.get(domain, budget_allocation['general_purpose'])
        breakdown = {}
        for component, percentage in allocation.items():
            breakdown[component] = round(budget * percentage / 100, 2)
        
        # Minimum budget requirements in INR. Public AI endpoints accept INR
        # budgets, even though the legacy fallback catalogue is stored in USD.
        min_budgets = {
            'gaming': 50000,
            'video_editing': 125000,
            'programming': 60000,
            'streaming': 100000,
            'rendering': 200000,
            'general_purpose': 35000
        }
        
        min_budget = min_budgets.get(domain, 500)
        
        if budget < min_budget:
            return {
                'sufficient': False,
                'message': f'Budget insufficient. Minimum recommended: ₹{int(min_budget*83):,}. Your budget: ₹{int(budget*83):,}',
                'budget_breakdown': breakdown,
                'message': f'Budget insufficient. Minimum recommended: Rs. {int(min_budget):,}. Your budget: Rs. {int(budget):,}',
                'budget_deficit': min_budget - budget,
                'currency': 'INR'
            }
        
        return {
            'sufficient': True,
            'message': f'Budget is sufficient for {domain_specs["name"]}',
            'budget_breakdown': breakdown,
            'budget_deficit': 0
        }
    
    @staticmethod
    def get_ai_suggestion(domain, game_name, budget):
        """
        Generate AI-suggested PC build based on domain, game, and budget.
        Uses PCBuildAgent for real Indian market pricing in INR.
        Caches results to speed up repeated requests.
        
        Returns: {
            success: bool,
            message: str,
            budget_check: dict,
            suggested_parts: dict (cpu, gpu, motherboard, ram, storage, psu, case, cooling),
            total_price: float,
            compatibility: dict,
            currency: str (INR),
            price_source: str
        }
        """
        # Create cache key from request parameters
        cache_key = f"{domain}_{game_name or 'no-game'}_{budget}"
        cache_hash = hashlib.md5(cache_key.encode()).hexdigest()
        
        # Check if result is in cache and not expired
        if cache_hash in AIBuildService._build_cache:
            cached_data = AIBuildService._build_cache[cache_hash]
            if time.time() - cached_data['timestamp'] < AIBuildService._cache_timeout:
                # Return cached result
                return cached_data['result']
        
        # Not in cache, generate fresh result
        pcbuild_result = PCBuildAgent.generate_build(domain, budget, game_name)
        
        if pcbuild_result['success']:
            # PCBuildAgent provided real Indian market pricing
            suggested_parts = {}
            
            # Convert PCBuildAgent format to AI suggestion format
            # Note: PCBuildAgent uses 'cooler' but we standardize to 'cooling'
            for category, part in pcbuild_result['parts'].items():
                # Rename 'cooler' to 'cooling' for consistency
                standard_category = 'cooling' if category == 'cooler' else category
                
                if part and isinstance(part, dict) and part.get('name'):
                    suggested_parts[standard_category] = {
                        'id': 0,  # PCBuild Agent doesn't use database IDs
                        'name': part['name'],
                        'price': part['price_inr'],
                        'price_inr': part['price_inr'],
                        'price_source': part.get('price_source', 'PCBuild Agent'),
                        'confidence': part.get('confidence', 'medium'),
                        'specs': part.get('specs', ''),
                        'note': part.get('note', '')
                    }
                else:
                    suggested_parts[standard_category] = None
            
            compatibility_parts = dict(suggested_parts)
            compatibility_parts['cooler'] = compatibility_parts.get('cooling')
            compatibility = AIBuildService._assess_catalogue_compatibility(compatibility_parts)
            
            result = {
                'success': True,
                'message': f'AI build suggestion for {domain} with budget Rs. {budget:,}',
                'budget_check': {
                    'sufficient': True,
                    'message': 'Budget is sufficient'
                },
                'suggested_parts': suggested_parts,
                'total_price': pcbuild_result['total_with_buffer'],
                'compatibility': compatibility,
                'game_name': game_name,
                'domain': domain,
                'budget': budget,
                'currency': 'INR',
                'price_source': 'Indian Market (PCBuild Agent)',
                'validation_logs': pcbuild_result['validation_logs']
            }
            
            # Cache the result
            AIBuildService._build_cache[cache_hash] = {
                'result': result,
                'timestamp': time.time()
            }
            
            return result
        
        # Fallback to original database-based recommendation if PCBuildAgent fails
        # Check budget first
        budget_check = AIBuildService.analyze_budget(domain, budget)
        if not budget_check['sufficient']:
            return {
                'success': False,
                'message': budget_check['message'],
                'budget_check': budget_check,
                'suggested_parts': {},
                'total_price': 0,
                'compatibility': {}
            }
        
        # Get domain specs
        domain_specs = AIBuildService.DOMAINS.get(domain)
        
        # Convert INR budget back to USD for database queries (1 USD = 83 INR)
        budget_usd = budget / 83
        
        # Budget allocation per domain (in percentage)
        budget_allocation = {
            'gaming': {'cpu': 20, 'gpu': 40, 'motherboard': 10, 'ram': 15, 'storage': 5, 'psu': 5, 'case': 3, 'cooling': 2},
            'video_editing': {'cpu': 35, 'gpu': 25, 'motherboard': 10, 'ram': 20, 'storage': 5, 'psu': 3, 'case': 1, 'cooling': 1},
            'programming': {'cpu': 30, 'gpu': 10, 'motherboard': 10, 'ram': 25, 'storage': 15, 'psu': 5, 'case': 3, 'cooling': 2},
            'streaming': {'cpu': 30, 'gpu': 30, 'motherboard': 10, 'ram': 15, 'storage': 5, 'psu': 5, 'case': 3, 'cooling': 2},
            'rendering': {'cpu': 25, 'gpu': 45, 'motherboard': 10, 'ram': 12, 'storage': 3, 'psu': 3, 'case': 1, 'cooling': 1},
            'general_purpose': {'cpu': 25, 'gpu': 15, 'motherboard': 12, 'ram': 20, 'storage': 15, 'psu': 8, 'case': 3, 'cooling': 2}
        }
        allocation = budget_allocation.get(domain, budget_allocation['general_purpose'])
        
        # Query database for best-fit parts
        with get_db() as conn:
            cursor = conn.cursor()
            
            # Select CPU based on domain priority and budget (in USD)
            cpu_budget_pct = allocation.get('cpu', 20)
            cpu_budget = budget_usd * cpu_budget_pct / 100
            if domain_specs['priority'] == 'cpu':
                cpu_budget *= 1.3  # Allocate more for CPU
            
            cpu_query = '''
                SELECT * FROM cpu 
                WHERE cores >= ? AND price <= ?
                ORDER BY cores DESC, turbo_clock DESC
                LIMIT 1
            '''
            cursor.execute(cpu_query, (domain_specs['min_cpu_cores'], cpu_budget))
            cpu_row = cursor.fetchone()
            cpu = dict(cpu_row) if cpu_row else None
            
            # Select GPU based on domain priority and budget (in USD)
            gpu_budget_pct = allocation.get('gpu', 40)
            gpu_budget = budget_usd * gpu_budget_pct / 100
            if domain_specs['priority'] == 'gpu':
                gpu_budget *= 1.3  # Allocate more for GPU
            
            gpu_query = '''
                SELECT * FROM gpu 
                WHERE vram_gb >= ? AND price <= ?
                ORDER BY vram_gb DESC, memory_speed_mhz DESC
                LIMIT 1
            '''
            cursor.execute(gpu_query, (domain_specs['min_gpu_vram'], gpu_budget))
            gpu_row = cursor.fetchone()
            gpu = dict(gpu_row) if gpu_row else None
            
            # Select compatible motherboard (in USD)
            motherboard_budget_pct = allocation.get('motherboard', 10)
            motherboard_budget = budget_usd * motherboard_budget_pct / 100
            socket_type = cpu['socket_type'] if cpu else 'LGA1700'
            
            motherboard_query = '''
                SELECT * FROM motherboard 
                WHERE socket_type = ? AND price <= ?
                ORDER BY price DESC
                LIMIT 1
            '''
            cursor.execute(motherboard_query, (socket_type, motherboard_budget))
            motherboard_row = cursor.fetchone()
            motherboard = dict(motherboard_row) if motherboard_row else None
            
            # If motherboard not found with budget constraint, increase budget
            if not motherboard:
                motherboard_query = '''
                    SELECT * FROM motherboard 
                    WHERE socket_type = ?
                    ORDER BY price ASC
                    LIMIT 1
                '''
                cursor.execute(motherboard_query, (socket_type,))
                motherboard_row = cursor.fetchone()
                motherboard = dict(motherboard_row) if motherboard_row else None
            
            # Select RAM based on motherboard compatibility (in USD)
            ram_budget_pct = allocation.get('ram', 15)
            ram_budget = budget_usd * ram_budget_pct / 100
            ram_type = motherboard['ram_type'] if motherboard else 'DDR5'
            
            ram_query = '''
                SELECT * FROM ram 
                WHERE type = ? AND size_gb >= ? AND price <= ?
                ORDER BY size_gb DESC, speed_mhz DESC
                LIMIT 1
            '''
            cursor.execute(ram_query, (ram_type, domain_specs['min_ram_gb'], ram_budget))
            ram_row = cursor.fetchone()
            ram = dict(ram_row) if ram_row else None
            
            # Select Storage (in USD)
            storage_budget_pct = allocation.get('storage', 5)
            storage_budget = budget_usd * storage_budget_pct / 100
            # Increase budget to ensure we find a storage device
            storage_budget = max(storage_budget, 150)
            
            storage_query = '''
                SELECT * FROM storage 
                WHERE type = 'NVMe' AND capacity_gb >= ? AND price <= ?
                ORDER BY capacity_gb DESC
                LIMIT 1
            '''
            cursor.execute(storage_query, (domain_specs['min_storage_gb'], storage_budget))
            storage_row = cursor.fetchone()
            storage = dict(storage_row) if storage_row else None
            
            # If storage not found, try without the NVMe filter
            if not storage:
                storage_query = '''
                    SELECT * FROM storage 
                    WHERE capacity_gb >= ? AND price <= ?
                    ORDER BY capacity_gb DESC, price ASC
                    LIMIT 1
                '''
                cursor.execute(storage_query, (domain_specs['min_storage_gb'], storage_budget * 1.5))
                storage_row = cursor.fetchone()
                storage = dict(storage_row) if storage_row else None
            
            # Select PSU (in USD)
            psu_budget_pct = allocation.get('psu', 5)
            psu_budget = budget_usd * psu_budget_pct / 100
            psu_wattage = domain_specs['min_psu_wattage']
            
            psu_query = '''
                SELECT * FROM psu 
                WHERE wattage >= ? AND price <= ?
                ORDER BY wattage DESC
                LIMIT 1
            '''
            cursor.execute(psu_query, (psu_wattage, psu_budget))
            psu_row = cursor.fetchone()
            psu = dict(psu_row) if psu_row else None
            
            # Select Case (in USD)
            case_budget_pct = allocation.get('case', 3)
            case_budget = budget_usd * case_budget_pct / 100
            # Increase budget to ensure we find a case
            case_budget = max(case_budget, 80)
            
            case_query = '''
                SELECT * FROM pc_case 
                WHERE price <= ?
                ORDER BY max_gpu_length_mm DESC
                LIMIT 1
            '''
            cursor.execute(case_query, (case_budget,))
            case_row = cursor.fetchone()
            case = dict(case_row) if case_row else None
            
            # Select Cooling (in USD)
            cooling_budget_pct = allocation.get('cooling', 2)
            cooling_budget = budget_usd * cooling_budget_pct / 100
            # Increase budget to ensure we find cooling
            cooling_budget = max(cooling_budget, 60)
            
            socket_type = cpu['socket_type'] if cpu else 'LGA1700'
            
            cooling_query = '''
                SELECT * FROM cooling 
                WHERE socket_type = ? AND price <= ?
                ORDER BY tdp_rating DESC
                LIMIT 1
            '''
            cursor.execute(cooling_query, (socket_type, cooling_budget))
            cooling_row = cursor.fetchone()
            cooling = dict(cooling_row) if cooling_row else None
            
            # If cooling not found, try without socket type filter
            if not cooling:
                cooling_query = '''
                    SELECT * FROM cooling 
                    WHERE price <= ?
                    ORDER BY tdp_rating DESC
                    LIMIT 1
                '''
                cursor.execute(cooling_query, (cooling_budget * 1.5,))
                cooling_row = cursor.fetchone()
                cooling = dict(cooling_row) if cooling_row else None
        
        # Calculate total price (in USD, will be converted to INR for display)
        total_price_usd = sum([
            cpu['price'] if cpu else 0,
            gpu['price'] if gpu else 0,
            motherboard['price'] if motherboard else 0,
            ram['price'] if ram else 0,
            storage['price'] if storage else 0,
            psu['price'] if psu else 0,
            case['price'] if case else 0,
            cooling['price'] if cooling else 0
        ])
        
        # Convert total price to INR (1 USD = 83 INR)
        total_price = round(total_price_usd * 83, 2)
        
        # Prepare suggested parts dict with INR prices
        suggested_parts = {
            'cpu': {**cpu, 'price_inr': round(cpu['price'] * 83, 2)} if cpu else None,
            'gpu': {**gpu, 'price_inr': round(gpu['price'] * 83, 2)} if gpu else None,
            'motherboard': {**motherboard, 'price_inr': round(motherboard['price'] * 83, 2)} if motherboard else None,
            'ram': {**ram, 'price_inr': round(ram['price'] * 83, 2)} if ram else None,
            'storage': {**storage, 'price_inr': round(storage['price'] * 83, 2)} if storage else None,
            'psu': {**psu, 'price_inr': round(psu['price'] * 83, 2)} if psu else None,
            'case': {**case, 'price_inr': round(case['price'] * 83, 2)} if case else None,
            'cooling': {**cooling, 'price_inr': round(cooling['price'] * 83, 2)} if cooling else None
        }
        
        # Check compatibility
        compat_engine = CompatibilityEngine()
        compatibility = compat_engine.validate_build(
            cpu['id'] if cpu else None,
            motherboard['id'] if motherboard else None,
            gpu['id'] if gpu else None,
            psu['id'] if psu else None,
            case['id'] if case else None,
            ram['id'] if ram else None,
            cooling['id'] if cooling else None
        )
        
        # Handle None result from validate_build
        if compatibility is None:
            compatibility = {
                'compatible': False,
                'errors': ['Missing CPU or Motherboard'],
                'warnings': []
            }
        
        result = {
            'success': True,
            'message': f'AI build suggestion for {domain} with budget ₹{int(budget*83):,}',
            'budget_check': budget_check,
            'message': f'AI build suggestion for {domain} with budget Rs. {int(budget):,}',
            'suggested_parts': suggested_parts,
            'total_price': round(total_price, 2),
            'compatibility': compatibility,
            'game_name': game_name,
            'domain': domain,
            'budget': budget,
            'currency': 'INR',
            'price_source': 'Local reference catalogue (USD converted at Rs. 83/USD)'
        }
        
        # Cache the result
        AIBuildService._build_cache[cache_hash] = {
            'result': result,
            'timestamp': time.time()
        }
        
        return result
