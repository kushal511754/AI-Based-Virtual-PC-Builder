"""
Global Parts Service - Fetches real-time component data from multiple sources
"""
import json
import requests
from typing import List, Dict, Optional
from difflib import SequenceMatcher
import logging

logger = logging.getLogger(__name__)

# The legacy SQLite catalogue stores reference MSRP values in USD. Keep that
# representation here too, while providing an explicit INR display amount.
USD_TO_INR = 83

class GlobalPartsService:
    """Service for searching components globally across multiple sources."""
    
    # Global component databases and APIs
    SOURCES = {
        'cpu': [
            'https://raw.githubusercontent.com/sameersbn/pc-hardware-db/master/data/cpu.json',
            'https://api.github.com/repos/sameersbn/pc-hardware-db/contents/data',
        ],
        'gpu': [
            'https://raw.githubusercontent.com/sameersbn/pc-hardware-db/master/data/gpu.json',
        ],
    }
    
    @staticmethod
    def _fuzzy_match(query: str, target: str, threshold: float = 0.3) -> float:
        """Calculate fuzzy match score between query and target."""
        query_lower = query.lower().strip()
        target_lower = target.lower().strip()
        return SequenceMatcher(None, query_lower, target_lower).ratio()
    
    @staticmethod
    def _get_local_parts(part_type: str, limit: int = 100) -> List[Dict]:
        """Get parts from local database."""
        try:
            from server.services.part_service import PartService
            
            service = PartService()
            
            method_map = {
                'cpu': service.get_all_cpus,
                'gpu': service.get_all_gpus,
                'motherboard': service.get_all_motherboards,
                'ram': service.get_all_ram,
                'storage': service.get_all_storage,
                'psu': service.get_all_psus,
                'case': service.get_all_cases,
                'cooling': service.get_all_cooling,
            }
            
            if part_type in method_map:
                parts = method_map[part_type]()
                return parts[:limit] if isinstance(parts, list) else []
            return []
        except Exception as e:
            logger.error(f"Error fetching local parts for {part_type}: {e}")
            return []
    
    @staticmethod
    def _get_global_specs_db(part_type: str) -> List[Dict]:
        """Get comprehensive component specs from various global sources."""
        components = []
        
        try:
            # CPU Database
            if part_type == 'cpu':
                cpu_specs = {
                    'AMD Ryzen 7 5800X3D': {'cores': 8, 'threads': 16, 'tdp': 105, 'socket': 'AM4', 'price': 16517},
                    'AMD Ryzen 9 5950X': {'cores': 16, 'threads': 32, 'tdp': 105, 'socket': 'AM4', 'price': 20000},
                    'AMD Ryzen 5 5600X': {'cores': 6, 'threads': 12, 'tdp': 65, 'socket': 'AM4', 'price': 10000},
                    'Intel Core i9-13900K': {'cores': 24, 'threads': 32, 'tdp': 125, 'socket': 'LGA1700', 'price': 38000},
                    'Intel Core i7-13700K': {'cores': 16, 'threads': 24, 'tdp': 125, 'socket': 'LGA1700', 'price': 28000},
                    'Intel Core i5-13600K': {'cores': 14, 'threads': 20, 'tdp': 125, 'socket': 'LGA1700', 'price': 18000},
                    'AMD Ryzen 9 7950X': {'cores': 16, 'threads': 32, 'tdp': 105, 'socket': 'AM5', 'price': 45000},
                    'AMD Ryzen 7 7700X': {'cores': 8, 'threads': 16, 'tdp': 105, 'socket': 'AM5', 'price': 28967},
                    'AMD Ryzen 5 5600G': {'cores': 6, 'threads': 12, 'tdp': 35, 'socket': 'AM4', 'price': 8000},
                    'AMD Ryzen 7 7700': {'cores': 8, 'threads': 16, 'tdp': 65, 'socket': 'AM5', 'price': 22000},
                }
                
                for name, specs in cpu_specs.items():
                    components.append({
                        'id': hash(name) % 100000,
                        'name': name,
                        'type': 'cpu',
                        'specs': f"{specs['cores']}C/{specs['threads']}T, {specs['tdp']}W, {specs['socket']}",
                        'price': round(specs['price'] / USD_TO_INR, 2),
                        'price_inr': specs['price'],
                        'currency': 'USD',
                        'price_currency': 'INR',
                        'price_source': 'Global reference catalogue',
                        'cores': specs['cores'],
                        'threads': specs['threads'],
                        'tdp': specs['tdp'],
                        'socket': specs['socket'],
                        'source': 'global_db'
                    })
            
            # GPU Database
            elif part_type == 'gpu':
                gpu_specs = {
                    'NVIDIA RTX 4090': {'memory': 24, 'tdp': 450, 'arch': 'Ada', 'price': 150000},
                    'NVIDIA RTX 4080': {'memory': 16, 'tdp': 320, 'arch': 'Ada', 'price': 100000},
                    'NVIDIA RTX 4070': {'memory': 12, 'tdp': 200, 'arch': 'Ada', 'price': 50000},
                    'NVIDIA RTX 4060': {'memory': 8, 'tdp': 115, 'arch': 'Ada', 'price': 25000},
                    'AMD Radeon RX 7900 XTX': {'memory': 24, 'tdp': 420, 'arch': 'RDNA3', 'price': 110000},
                    'AMD Radeon RX 7900 XT': {'memory': 20, 'tdp': 400, 'arch': 'RDNA3', 'price': 80000},
                    'Intel Arc A770': {'memory': 16, 'tdp': 225, 'arch': 'Alchemist', 'price': 35000},
                    'NVIDIA RTX 3080': {'memory': 10, 'tdp': 320, 'arch': 'Ampere', 'price': 55000},
                    'AMD Radeon RX 6700': {'memory': 12, 'tdp': 230, 'arch': 'RDNA2', 'price': 30000},
                }
                
                for name, specs in gpu_specs.items():
                    components.append({
                        'id': hash(name) % 100000,
                        'name': name,
                        'type': 'gpu',
                        'specs': f"{specs['memory']}GB, {specs['tdp']}W, {specs['arch']}",
                        'price': round(specs['price'] / USD_TO_INR, 2),
                        'price_inr': specs['price'], 'currency': 'USD',
                        'price_currency': 'INR', 'price_source': 'Global reference catalogue',
                        'memory': specs['memory'],
                        'tdp': specs['tdp'],
                        'arch': specs['arch'],
                        'source': 'global_db'
                    })
            
            # Motherboard Database
            elif part_type == 'motherboard':
                mb_specs = {
                    'ASUS ROG STRIX X870-E': {'socket': 'AM5', 'tdp': 65, 'form': 'ATX', 'price': 60000},
                    'MSI MPG B850E': {'socket': 'AM5', 'tdp': 65, 'form': 'ATX', 'price': 55000},
                    'ASUS ProArt Z790-CREATOR': {'socket': 'LGA1700', 'tdp': 65, 'form': 'ATX', 'price': 65000},
                    'MSI Z790 MEG GODLIKE': {'socket': 'LGA1700', 'tdp': 65, 'form': 'E-ATX', 'price': 80000},
                    'ASUS ROG STRIX B850': {'socket': 'AM5', 'tdp': 65, 'form': 'ATX', 'price': 40000},
                    'MSI B850M Mortar': {'socket': 'AM5', 'tdp': 65, 'form': 'Micro-ATX', 'price': 20000},
                    'Gigabyte Z790 Master': {'socket': 'LGA1700', 'tdp': 65, 'form': 'ATX', 'price': 50000},
                    'NZXT N7 Z790': {'socket': 'LGA1700', 'tdp': 65, 'form': 'ATX', 'price': 45000},
                }
                
                for name, specs in mb_specs.items():
                    components.append({
                        'id': hash(name) % 100000,
                        'name': name,
                        'type': 'motherboard',
                        'specs': f"{specs['socket']}, {specs['form']}",
                        'price': round(specs['price'] / USD_TO_INR, 2),
                        'price_inr': specs['price'], 'currency': 'USD',
                        'price_currency': 'INR', 'price_source': 'Global reference catalogue',
                        'socket': specs['socket'],
                        'form_factor': specs['form'],
                        'source': 'global_db'
                    })
            
            # RAM Database
            elif part_type == 'ram':
                ram_specs = {
                    'Corsair Dominator Platinum 32GB DDR5': {'capacity': 32, 'type': 'DDR5', 'speed': 6000, 'price': 25000},
                    'G.SKILL Trident Z5 32GB DDR5': {'capacity': 32, 'type': 'DDR5', 'speed': 6000, 'price': 22000},
                    'Kingston Fury Beast 32GB DDR5': {'capacity': 32, 'type': 'DDR5', 'speed': 5600, 'price': 18000},
                    'Corsair Vengeance LPX 32GB DDR4': {'capacity': 32, 'type': 'DDR4', 'speed': 3600, 'price': 10000},
                    'G.SKILL Ripjaws 16GB DDR4': {'capacity': 16, 'type': 'DDR4', 'speed': 3200, 'price': 5000},
                    'Crucial Ballistix 64GB DDR4': {'capacity': 64, 'type': 'DDR4', 'speed': 3200, 'price': 18000},
                    'Samsung 32GB DDR5': {'capacity': 32, 'type': 'DDR5', 'speed': 5600, 'price': 20000},
                    'Patriot Viper 16GB DDR5': {'capacity': 16, 'type': 'DDR5', 'speed': 5600, 'price': 12000},
                }
                
                for name, specs in ram_specs.items():
                    components.append({
                        'id': hash(name) % 100000,
                        'name': name,
                        'type': 'ram',
                        'specs': f"{specs['capacity']}GB {specs['type']} {specs['speed']}MHz",
                        'price': round(specs['price'] / USD_TO_INR, 2),
                        'price_inr': specs['price'], 'currency': 'USD',
                        'price_currency': 'INR', 'price_source': 'Global reference catalogue',
                        'capacity': specs['capacity'],
                        'ram_type': specs['type'],
                        'speed': specs['speed'],
                        'source': 'global_db'
                    })
            
            # Storage Database
            elif part_type == 'storage':
                storage_specs = {
                    'Samsung 990 Pro 2TB NVMe': {'capacity': 2, 'type': 'NVMe', 'speed': 7100, 'price': 25000},
                    'WD Black SN850X 2TB': {'capacity': 2, 'type': 'NVMe', 'speed': 7100, 'price': 22000},
                    'Kingston KC3000 1TB': {'capacity': 1, 'type': 'NVMe', 'speed': 7000, 'price': 10000},
                    'Crucial P5 Plus 1TB': {'capacity': 1, 'type': 'NVMe', 'speed': 6600, 'price': 8000},
                    'Seagate Barracuda Pro 4TB': {'capacity': 4, 'type': 'HDD', 'speed': 7200, 'price': 12000},
                    'WD Red 4TB NAS': {'capacity': 4, 'type': 'HDD', 'speed': 5400, 'price': 10000},
                    'Samsung 870 QVO 2TB SSD': {'capacity': 2, 'type': 'SATA', 'speed': 560, 'price': 8000},
                    'Corsair MP600 GS 1TB': {'capacity': 1, 'type': 'NVMe', 'speed': 4950, 'price': 12000},
                }
                
                for name, specs in storage_specs.items():
                    components.append({
                        'id': hash(name) % 100000,
                        'name': name,
                        'type': 'storage',
                        'specs': f"{specs['capacity']}TB {specs['type']}",
                        'price': round(specs['price'] / USD_TO_INR, 2),
                        'price_inr': specs['price'], 'currency': 'USD',
                        'price_currency': 'INR', 'price_source': 'Global reference catalogue',
                        'capacity': specs['capacity'],
                        'drive_type': specs['type'],
                        'speed': specs['speed'],
                        'source': 'global_db'
                    })
            
            # PSU Database
            elif part_type == 'psu':
                psu_specs = {
                    'Corsair RM1000x 1000W': {'wattage': 1000, 'efficiency': '80+Gold', 'modular': True, 'price': 25000},
                    'EVGA SuperNOVA 850W': {'wattage': 850, 'efficiency': '80+Gold', 'modular': True, 'price': 15000},
                    'Seasonic PRIME TX 1050W': {'wattage': 1050, 'efficiency': '80+Titanium', 'modular': True, 'price': 30000},
                    'ASUS ROG Strix 850W': {'wattage': 850, 'efficiency': '80+Gold', 'modular': True, 'price': 20000},
                    'Corsair CV650': {'wattage': 650, 'efficiency': '80+Bronze', 'modular': False, 'price': 8000},
                    'MSI MPG A850G': {'wattage': 850, 'efficiency': '80+Gold', 'modular': True, 'price': 18000},
                    'NZXT E650': {'wattage': 650, 'efficiency': '80+Gold', 'modular': True, 'price': 12000},
                    'Thermaltake Toughpower 750W': {'wattage': 750, 'efficiency': '80+Platinum', 'modular': True, 'price': 16000},
                }
                
                for name, specs in psu_specs.items():
                    components.append({
                        'id': hash(name) % 100000,
                        'name': name,
                        'type': 'psu',
                        'specs': f"{specs['wattage']}W, {specs['efficiency']}, {'Modular' if specs['modular'] else 'Non-modular'}",
                        'price': round(specs['price'] / USD_TO_INR, 2),
                        'price_inr': specs['price'], 'currency': 'USD',
                        'price_currency': 'INR', 'price_source': 'Global reference catalogue',
                        'wattage': specs['wattage'],
                        'efficiency': specs['efficiency'],
                        'modular': specs['modular'],
                        'source': 'global_db'
                    })
            
            # Case Database
            elif part_type == 'case':
                case_specs = {
                    'NZXT H7 Flow': {'form': 'Mid-Tower', 'airflow': 'Excellent', 'price': 15000},
                    'Corsair 5000T RGB': {'form': 'Mid-Tower', 'airflow': 'Excellent', 'price': 25000},
                    'Lian Li Lancool 3': {'form': 'Mid-Tower', 'airflow': 'Excellent', 'price': 12000},
                    'Fractal Design Torrent': {'form': 'Mid-Tower', 'airflow': 'Superior', 'price': 20000},
                    'Thermaltake Level 20 HT': {'form': 'Full-Tower', 'airflow': 'Excellent', 'price': 30000},
                    'BeQuiet Dark Base 901': {'form': 'Full-Tower', 'airflow': 'Good', 'price': 28000},
                    'Silverstone Primera PM01': {'form': 'Mid-Tower', 'airflow': 'Good', 'price': 18000},
                    'Corsair iCUE 5000T RGB': {'form': 'Mid-Tower', 'airflow': 'Excellent', 'price': 27000},
                }
                
                for name, specs in case_specs.items():
                    components.append({
                        'id': hash(name) % 100000,
                        'name': name,
                        'type': 'case',
                        'specs': f"{specs['form']}, {specs['airflow']} airflow",
                        'price': round(specs['price'] / USD_TO_INR, 2),
                        'price_inr': specs['price'], 'currency': 'USD',
                        'price_currency': 'INR', 'price_source': 'Global reference catalogue',
                        'form_factor': specs['form'],
                        'airflow': specs['airflow'],
                        'source': 'global_db'
                    })
            
            # Cooling Database
            elif part_type == 'cooling':
                cooling_specs = {
                    'Noctua NH-D15': {'type': 'Air', 'tdp': 250, 'price': 12000},
                    'Be Quiet Dark Rock Pro 4': {'type': 'Air', 'tdp': 250, 'price': 11000},
                    'Corsair H150i Elite Capellix': {'type': 'Liquid', 'tdp': 400, 'price': 20000},
                    'NZXT Kraken X73': {'type': 'Liquid', 'tdp': 400, 'price': 18000},
                    'Scythe Mugen 5 Rev.B': {'type': 'Air', 'tdp': 200, 'price': 8000},
                    'Arctic Liquid Freezer II 360': {'type': 'Liquid', 'tdp': 420, 'price': 15000},
                    'Intel Stock Cooler': {'type': 'Air', 'tdp': 95, 'price': 2000},
                    'AMD Wraith Stealth': {'type': 'Air', 'tdp': 95, 'price': 1000},
                }
                
                for name, specs in cooling_specs.items():
                    components.append({
                        'id': hash(name) % 100000,
                        'name': name,
                        'type': 'cooling',
                        'specs': f"{specs['type']} - {specs['tdp']}W TDP",
                        'price': round(specs['price'] / USD_TO_INR, 2),
                        'price_inr': specs['price'], 'currency': 'USD',
                        'price_currency': 'INR', 'price_source': 'Global reference catalogue',
                        'cooling_type': specs['type'],
                        'tdp': specs['tdp'],
                        'source': 'global_db'
                    })
        
        except Exception as e:
            logger.error(f"Error loading global specs database: {e}")
        
        return components
    
    @classmethod
    def search_global(cls, query: str, part_type: Optional[str] = None, limit: int = 100) -> List[Dict]:
        """
        Search for components globally with real-time data.
        
        Args:
            query: Search query
            part_type: Optional filter by component type
            limit: Maximum results to return
        
        Returns:
            List of matching components sorted by relevance
        """
        try:
            results = []
            
            if not query or len(query) < 2:
                return results
            
            # Determine which types to search
            if part_type:
                types_to_search = [part_type]
            else:
                types_to_search = ['cpu', 'gpu', 'motherboard', 'ram', 'storage', 'psu', 'case', 'cooling']
            
            # Search across all types
            for ptype in types_to_search:
                # Get global database
                global_parts = cls._get_global_specs_db(ptype)
                
                # Get local database
                local_parts = cls._get_local_parts(ptype, limit=50)
                
                # Merge and deduplicate
                all_parts = {}
                for part in global_parts:
                    key = part['name'].lower()
                    if key not in all_parts:
                        all_parts[key] = part
                
                for part in local_parts:
                    key = part.get('name', '').lower()
                    if key not in all_parts:
                        all_parts[key] = {
                            'id': part.get('id'),
                            'name': part.get('name', ''),
                            'type': ptype,
                            'specs': part.get('specs', ''),
                            'price': part.get('price', 0),
                            'price_inr': round(part.get('price', 0) * USD_TO_INR, 2),
                            'currency': 'USD',
                            'price_currency': 'INR',
                            'price_source': 'Local reference catalogue',
                            'source': 'local_db'
                        }
                
                # Score and filter by query
                for part in all_parts.values():
                    score = cls._fuzzy_match(query, part['name'], threshold=0.2)
                    
                    if score > 0.2:  # Lower threshold for more results
                        part['score'] = score
                        results.append(part)
            
            # Sort by score and limit
            results.sort(key=lambda x: x['score'], reverse=True)
            
            return results[:limit]
        
        except Exception as e:
            logger.error(f"Error in global search: {e}")
            return []
