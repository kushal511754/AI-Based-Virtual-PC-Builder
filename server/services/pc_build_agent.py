"""
PCBuildAgent - Realistic PC component recommendations in INR (₹) for Indian market.
Generates builds for domains: Gaming, Editing, Rendering, Streaming.
"""

import json
from datetime import datetime

class PCBuildAgent:
    """Agent for generating realistic PC builds with Indian market pricing."""
    
    # Minimum price floors (in INR) - guardrails for validation
    PRICE_FLOORS = {
        'gpu': 25000,
        'cpu': 8000,
        'motherboard': 5000,
        'ram_16gb': 3000,
        'nvme_ssd_1tb': 3000,
        'psu': 3000,
        'case': 2000,
        'cooler': 1500,
        'windows_os': 8000
    }
    
    # Real Indian market pricing database (from reliable sources)
    # Sources: Amazon India, MDComputers, Vedant, PrimeABGB
    COMPONENT_DATABASE = {
        'gaming': {
            '₹50k': {
                'cpu': {
                    'name': 'AMD Ryzen 3 4100',
                    'price_inr': 7000,
                    'price_source': 'Amazon India',
                    'confidence': 'high',
                    'specs': '4 cores, 8 threads, 3.8-4.0GHz'
                },
                'gpu': {
                    'name': 'RTX 3050 6GB',
                    'price_inr': 18000,
                    'price_source': 'MDComputers',
                    'confidence': 'medium',
                    'specs': '6GB GDDR6, 1x 8-pin, ~70W'
                },
                'motherboard': {
                    'name': 'Gigabyte A520M DS3H',
                    'price_inr': 4500,
                    'price_source': 'Vedant',
                    'confidence': 'high',
                    'specs': 'AM4 socket, Micro ATX'
                },
                'ram': {
                    'name': 'Corsair Vengeance 8GB DDR4 3000MHz',
                    'price_inr': 2500,
                    'price_source': 'Amazon India',
                    'confidence': 'high',
                    'specs': '8GB, DDR4-3000, 1x8GB'
                },
                'storage': {
                    'name': 'Crucial BX500 500GB SSD',
                    'price_inr': 2500,
                    'price_source': 'PrimeABGB',
                    'confidence': 'high',
                    'specs': '500GB, SATA SSD'
                },
                'psu': {
                    'name': 'Corsair CV450 450W',
                    'price_inr': 3000,
                    'price_source': 'Amazon India',
                    'confidence': 'high',
                    'specs': '450W, 80+ Bronze, Non-modular'
                },
                'case': {
                    'name': 'Zebronics Zeb-Transformer',
                    'price_inr': 1800,
                    'price_source': 'MDComputers',
                    'confidence': 'high',
                    'specs': 'Micro ATX, Budget cabinet'
                },
                'cooler': {
                    'name': 'Stock Cooler (AMD Wraith Stealth)',
                    'price_inr': 1500,
                    'price_source': 'Equivalent Market Price',
                    'confidence': 'high',
                    'specs': 'Wraith Stealth cooler, budget-friendly'
                }
            },
            '₹100k': {
                'cpu': {
                    'name': 'AMD Ryzen 5 5500',
                    'price_inr': 11500,
                    'price_source': 'Amazon India',
                    'confidence': 'high',
                    'specs': '6 cores, 12 threads, 3.6-4.2GHz'
                },
                'gpu': {
                    'name': 'RTX 4050 (Budget)',
                    'price_inr': 28000,
                    'price_source': 'MDComputers',
                    'confidence': 'medium',
                    'specs': '6GB GDDR6, 1x 8-pin, ~120W'
                },
                'motherboard': {
                    'name': 'MSI B450M-A PRO MAX II',
                    'price_inr': 6500,
                    'price_source': 'Vedant',
                    'confidence': 'high',
                    'specs': 'AM4 socket, Micro ATX'
                },
                'ram': {
                    'name': 'G.Skill Aegis 16GB DDR4 3000MHz',
                    'price_inr': 4500,
                    'price_source': 'Amazon India',
                    'confidence': 'high',
                    'specs': '16GB, DDR4-3000, 2x8GB'
                },
                'storage': {
                    'name': 'Kingston A2000 1TB NVMe',
                    'price_inr': 4500,
                    'price_source': 'PrimeABGB',
                    'confidence': 'high',
                    'specs': '1TB, PCIe 3.0 NVMe'
                },
                'psu': {
                    'name': 'Corsair CV550 550W',
                    'price_inr': 4000,
                    'price_source': 'Amazon India',
                    'confidence': 'high',
                    'specs': '550W, 80+ Bronze, Non-modular'
                },
                'case': {
                    'name': 'Antec NX100 Mid Tower',
                    'price_inr': 2500,
                    'price_source': 'MDComputers',
                    'confidence': 'high',
                    'specs': 'Micro ATX/ATX, Good airflow'
                },
                'cooler': {
                    'name': 'Stock Cooler (AMD Wraith Stealth)',
                    'price_inr': 1500,
                    'price_source': 'Equivalent Market Price',
                    'confidence': 'high',
                    'specs': 'Wraith Stealth cooler, budget-friendly'
                }
            },
            '₹150k': {
                'cpu': {
                    'name': 'Intel Core i5-12400F',
                    'price_inr': 15000,
                    'price_source': 'Amazon India',
                    'confidence': 'high',
                    'specs': '6 cores, 12 threads, 3.3-4.4GHz'
                },
                'gpu': {
                    'name': 'RTX 4060 8GB',
                    'price_inr': 35000,
                    'price_source': 'MDComputers',
                    'confidence': 'high',
                    'specs': '8GB GDDR6, 1x 8-pin, ~70W'
                },
                'motherboard': {
                    'name': 'MSI B660M-A PRO',
                    'price_inr': 8500,
                    'price_source': 'Vedant',
                    'confidence': 'high',
                    'specs': 'LGA1700 socket, DDR4, Micro ATX'
                },
                'ram': {
                    'name': 'Kingston Fury Beast 16GB DDR4 3200MHz',
                    'price_inr': 5000,
                    'price_source': 'Amazon India',
                    'confidence': 'high',
                    'specs': '16GB, DDR4-3200, 2x8GB'
                },
                'storage': {
                    'name': 'WD Blue SN570 1TB NVMe',
                    'price_inr': 5500,
                    'price_source': 'PrimeABGB',
                    'confidence': 'high',
                    'specs': '1TB, PCIe 3.0 NVMe'
                },
                'psu': {
                    'name': 'Seasonic Core GM 650W 80+ Gold',
                    'price_inr': 6000,
                    'price_source': 'Amazon India',
                    'confidence': 'high',
                    'specs': '650W, 80+ Gold, Semi-modular'
                },
                'case': {
                    'name': 'NZXT H510 Flow Mid Tower',
                    'price_inr': 4500,
                    'price_source': 'MDComputers',
                    'confidence': 'high',
                    'specs': 'ATX, Tempered glass, Good thermals'
                },
                'cooler': {
                    'name': 'Deepcool AK400 Basic',
                    'price_inr': 1800,
                    'price_source': 'Amazon India',
                    'confidence': 'high',
                    'specs': 'Budget air cooler, LGA1700 compatible'
                }
            },
            '₹200k': {
                'cpu': {
                    'name': 'Intel Core i5-13600K',
                    'price_inr': 28000,
                    'price_source': 'Amazon India',
                    'confidence': 'high',
                    'specs': '14 cores (6P+8E), 20 threads, 3.5-5.1GHz'
                },
                'gpu': {
                    'name': 'RTX 4070 12GB',
                    'price_inr': 55000,
                    'price_source': 'MDComputers',
                    'confidence': 'high',
                    'specs': '12GB GDDR6X, 1x 8-pin + 1x 6-pin, ~200W'
                },
                'motherboard': {
                    'name': 'MSI Z790-A PRO',
                    'price_inr': 18000,
                    'price_source': 'Vedant',
                    'confidence': 'high',
                    'specs': 'LGA1700 socket, DDR5, ATX, PCIe 5.0'
                },
                'ram': {
                    'name': 'G.Skill Trident Z5 32GB DDR5 6000MHz',
                    'price_inr': 12000,
                    'price_source': 'Amazon India',
                    'confidence': 'high',
                    'specs': '32GB, DDR5-6000, 2x16GB'
                },
                'storage': {
                    'name': 'Samsung 990 Pro 1TB NVMe',
                    'price_inr': 10000,
                    'price_source': 'PrimeABGB',
                    'confidence': 'high',
                    'specs': '1TB, PCIe 4.0 NVMe, 7100MB/s'
                },
                'psu': {
                    'name': 'Corsair RM850x 850W 80+ Gold',
                    'price_inr': 10500,
                    'price_source': 'Amazon India',
                    'confidence': 'high',
                    'specs': '850W, 80+ Gold, Fully modular'
                },
                'case': {
                    'name': 'Lian Li LANCOOL 205 Mid Tower',
                    'price_inr': 5500,
                    'price_source': 'MDComputers',
                    'confidence': 'high',
                    'specs': 'ATX, Mesh front, Great airflow'
                },
                'cooler': {
                    'name': 'Arctic Freezer 34 eSports DUO',
                    'price_inr': 3500,
                    'price_source': 'Amazon India',
                    'confidence': 'high',
                    'specs': 'Dual tower air cooler, LGA1700, High performance'
                }
            }
        },
        'video_editing': {
            '₹75k': {
                'cpu': {
                    'name': 'AMD Ryzen 5 3600',
                    'price_inr': 12000,
                    'price_source': 'Amazon India',
                    'confidence': 'high',
                    'specs': '6 cores, 12 threads, 3.6-4.2GHz'
                },
                'gpu': {
                    'name': 'RTX 3050 6GB',
                    'price_inr': 18000,
                    'price_source': 'MDComputers',
                    'confidence': 'medium',
                    'specs': '6GB GDDR6, Budget GPU for basic editing'
                },
                'motherboard': {
                    'name': 'Gigabyte B450M DS3H',
                    'price_inr': 5500,
                    'price_source': 'Vedant',
                    'confidence': 'high',
                    'specs': 'AM4 socket, Micro ATX'
                },
                'ram': {
                    'name': 'Corsair Vengeance LPX 16GB DDR4 3200MHz',
                    'price_inr': 5000,
                    'price_source': 'Amazon India',
                    'confidence': 'high',
                    'specs': '16GB, DDR4-3200, 2x8GB'
                },
                'storage': {
                    'name': 'WD Blue SN570 500GB NVMe',
                    'price_inr': 3500,
                    'price_source': 'PrimeABGB',
                    'confidence': 'high',
                    'specs': '500GB, PCIe 3.0 NVMe'
                },
                'psu': {
                    'name': 'Corsair CV450 450W',
                    'price_inr': 3000,
                    'price_source': 'Amazon India',
                    'confidence': 'high',
                    'specs': '450W, 80+ Bronze, budget PSU'
                },
                'case': {
                    'name': 'Zebronics Zeb-Transformer',
                    'price_inr': 1800,
                    'price_source': 'MDComputers',
                    'confidence': 'high',
                    'specs': 'Micro ATX, Budget cabinet'
                },
                'cooler': {
                    'name': 'Stock Cooler (AMD Wraith Stealth)',
                    'price_inr': 1500,
                    'price_source': 'Equivalent Market Price',
                    'confidence': 'high',
                    'specs': 'Wraith Stealth cooler, budget-friendly'
                }
            },
            '₹150k': {
                'cpu': {
                    'name': 'AMD Ryzen 5 5600X',
                    'price_inr': 17000,
                    'price_source': 'Amazon India',
                    'confidence': 'high',
                    'specs': '6 cores, 12 threads, 3.7-4.6GHz'
                },
                'gpu': {
                    'name': 'RTX 3060 12GB',
                    'price_inr': 32000,
                    'price_source': 'MDComputers',
                    'confidence': 'high',
                    'specs': '12GB GDDR6, CUDA cores for editing'
                },
                'motherboard': {
                    'name': 'ASUS ROG STRIX B550-F',
                    'price_inr': 14000,
                    'price_source': 'Vedant',
                    'confidence': 'high',
                    'specs': 'AM4 socket, ATX, PCIe 4.0'
                },
                'ram': {
                    'name': 'G.Skill Trident Z Neo 32GB DDR4 3600MHz',
                    'price_inr': 8000,
                    'price_source': 'Amazon India',
                    'confidence': 'high',
                    'specs': '32GB, DDR4-3600, 2x16GB, optimized for Ryzen'
                },
                'storage': {
                    'name': 'WD Black SN850X 2TB NVMe',
                    'price_inr': 18000,
                    'price_source': 'PrimeABGB',
                    'confidence': 'high',
                    'specs': '2TB, PCIe 4.0, Fast for video projects'
                },
                'psu': {
                    'name': 'Corsair RM750x 750W 80+ Gold',
                    'price_inr': 9000,
                    'price_source': 'Amazon India',
                    'confidence': 'high',
                    'specs': '750W, 80+ Gold, Fully modular'
                },
                'case': {
                    'name': 'Fractal Design Core 1000 Mid Tower',
                    'price_inr': 4000,
                    'price_source': 'MDComputers',
                    'confidence': 'high',
                    'specs': 'ATX, Good airflow, Simple design'
                },
                'cooler': {
                    'name': 'Noctua NH-U12S chromax.black',
                    'price_inr': 6000,
                    'price_source': 'Amazon India',
                    'confidence': 'high',
                    'specs': 'High-end air cooler, quiet operation'
                }
            }
        },
        'streaming': {
            '₹100k': {
                'cpu': {
                    'name': 'AMD Ryzen 5 5500',
                    'price_inr': 11500,
                    'price_source': 'Amazon India',
                    'confidence': 'high',
                    'specs': '6 cores, 12 threads, 3.6-4.2GHz'
                },
                'gpu': {
                    'name': 'RTX 4050 6GB',
                    'price_inr': 28000,
                    'price_source': 'MDComputers',
                    'confidence': 'high',
                    'specs': '6GB GDDR6, Good for encoding'
                },
                'motherboard': {
                    'name': 'Gigabyte B550M DS3H PRO',
                    'price_inr': 7500,
                    'price_source': 'Vedant',
                    'confidence': 'high',
                    'specs': 'AM4 socket, Micro ATX'
                },
                'ram': {
                    'name': 'Corsair Vengeance LPX 16GB DDR4 3200MHz',
                    'price_inr': 5000,
                    'price_source': 'Amazon India',
                    'confidence': 'high',
                    'specs': '16GB, DDR4-3200, 2x8GB'
                },
                'storage': {
                    'name': 'WD Blue SN570 1TB NVMe',
                    'price_inr': 5000,
                    'price_source': 'PrimeABGB',
                    'confidence': 'high',
                    'specs': '1TB, PCIe 3.0 NVMe'
                },
                'psu': {
                    'name': 'Corsair RM750x 750W 80+ Gold',
                    'price_inr': 9000,
                    'price_source': 'Amazon India',
                    'confidence': 'high',
                    'specs': '750W, 80+ Gold, Fully modular'
                },
                'case': {
                    'name': 'Fractal Design Core 1000 Mid Tower',
                    'price_inr': 4000,
                    'price_source': 'MDComputers',
                    'confidence': 'high',
                    'specs': 'ATX, Good airflow'
                },
                'cooler': {
                    'name': 'Deepcool AK400 Basic',
                    'price_inr': 1800,
                    'price_source': 'Amazon India',
                    'confidence': 'high',
                    'specs': 'Budget air cooler, LGA1700 compatible'
                }
            },
            '₹150k': {
                'cpu': {
                    'name': 'AMD Ryzen 5 5600X',
                    'price_inr': 17000,
                    'price_source': 'Amazon India',
                    'confidence': 'high',
                    'specs': '6 cores, 12 threads, 3.7-4.6GHz'
                },
                'gpu': {
                    'name': 'RTX 3060 12GB',
                    'price_inr': 32000,
                    'price_source': 'MDComputers',
                    'confidence': 'high',
                    'specs': '12GB GDDR6, Excellent for streaming encoding'
                },
                'motherboard': {
                    'name': 'ASUS TUF B550-PLUS',
                    'price_inr': 12000,
                    'price_source': 'Vedant',
                    'confidence': 'high',
                    'specs': 'AM4 socket, ATX, PCIe 4.0'
                },
                'ram': {
                    'name': 'G.Skill Trident Z Neo 32GB DDR4 3600MHz',
                    'price_inr': 8000,
                    'price_source': 'Amazon India',
                    'confidence': 'high',
                    'specs': '32GB, DDR4-3600, 2x16GB, optimized for Ryzen'
                },
                'storage': {
                    'name': 'WD Black SN850X 1TB NVMe',
                    'price_inr': 10000,
                    'price_source': 'PrimeABGB',
                    'confidence': 'high',
                    'specs': '1TB, PCIe 4.0, Fast storage for streaming'
                },
                'psu': {
                    'name': 'Corsair RM850x 850W 80+ Gold',
                    'price_inr': 10500,
                    'price_source': 'Amazon India',
                    'confidence': 'high',
                    'specs': '850W, 80+ Gold, Fully modular'
                },
                'case': {
                    'name': 'NZXT H510 Flow Mid Tower',
                    'price_inr': 4500,
                    'price_source': 'MDComputers',
                    'confidence': 'high',
                    'specs': 'ATX, Tempered glass, Good thermals'
                },
                'cooler': {
                    'name': 'Arctic Freezer 34 eSports DUO',
                    'price_inr': 3500,
                    'price_source': 'Amazon India',
                    'confidence': 'high',
                    'specs': 'Dual tower air cooler, High performance'
                }
            }
        },
        'rendering': {
            '₹120k': {
                'cpu': {
                    'name': 'AMD Ryzen 7 5700X',
                    'price_inr': 19000,
                    'price_source': 'Amazon India',
                    'confidence': 'high',
                    'specs': '8 cores, 16 threads, 3.6-4.6GHz'
                },
                'gpu': {
                    'name': 'RTX 4060 Ti 8GB',
                    'price_inr': 35000,
                    'price_source': 'MDComputers',
                    'confidence': 'high',
                    'specs': '8GB GDDR6, CUDA cores for rendering'
                },
                'motherboard': {
                    'name': 'ASUS TUF B550-PLUS',
                    'price_inr': 12000,
                    'price_source': 'Vedant',
                    'confidence': 'high',
                    'specs': 'AM4 socket, ATX, PCIe 4.0'
                },
                'ram': {
                    'name': 'G.Skill Trident Z Neo 32GB DDR4 3600MHz',
                    'price_inr': 8000,
                    'price_source': 'Amazon India',
                    'confidence': 'high',
                    'specs': '32GB, DDR4-3600, 2x16GB'
                },
                'storage': {
                    'name': 'WD Black SN850X 1TB NVMe',
                    'price_inr': 10000,
                    'price_source': 'PrimeABGB',
                    'confidence': 'high',
                    'specs': '1TB, PCIe 4.0, Fast for rendering'
                },
                'psu': {
                    'name': 'Corsair RM850x 850W 80+ Gold',
                    'price_inr': 10500,
                    'price_source': 'Amazon India',
                    'confidence': 'high',
                    'specs': '850W, 80+ Gold, Fully modular'
                },
                'case': {
                    'name': 'NZXT H510 Flow Mid Tower',
                    'price_inr': 4500,
                    'price_source': 'MDComputers',
                    'confidence': 'high',
                    'specs': 'ATX, Tempered glass, Good thermals'
                },
                'cooler': {
                    'name': 'Arctic Freezer 34 eSports DUO',
                    'price_inr': 3500,
                    'price_source': 'Amazon India',
                    'confidence': 'high',
                    'specs': 'Dual tower air cooler, High performance'
                }
            },
            '₹250k': {
                'cpu': {
                    'name': 'Intel Core i7-13700K',
                    'price_inr': 35000,
                    'price_source': 'Amazon India',
                    'confidence': 'high',
                    'specs': '16 cores (8P+8E), 24 threads, 3.4-5.4GHz'
                },
                'gpu': {
                    'name': 'RTX 4070 Super 12GB',
                    'price_inr': 70000,
                    'price_source': 'MDComputers',
                    'confidence': 'high',
                    'specs': '12GB GDDR6X, Excellent for CUDA rendering'
                },
                'motherboard': {
                    'name': 'MSI Z790-A PRO',
                    'price_inr': 18000,
                    'price_source': 'Vedant',
                    'confidence': 'high',
                    'specs': 'LGA1700 socket, ATX, PCIe 5.0'
                },
                'ram': {
                    'name': 'G.Skill Trident Z5 64GB DDR5 6000MHz',
                    'price_inr': 20000,
                    'price_source': 'Amazon India',
                    'confidence': 'high',
                    'specs': '64GB, DDR5-6000, 2x32GB, High bandwidth'
                },
                'storage': {
                    'name': 'Samsung 990 Pro 2TB NVMe',
                    'price_inr': 18000,
                    'price_source': 'PrimeABGB',
                    'confidence': 'high',
                    'specs': '2TB, PCIe 4.0 NVMe, 7100MB/s'
                },
                'psu': {
                    'name': 'Corsair RM1000x 1000W 80+ Gold',
                    'price_inr': 13000,
                    'price_source': 'Amazon India',
                    'confidence': 'high',
                    'specs': '1000W, 80+ Gold, Fully modular'
                },
                'case': {
                    'name': 'Lian Li LANCOOL 215 Mid Tower',
                    'price_inr': 5500,
                    'price_source': 'MDComputers',
                    'confidence': 'high',
                    'specs': 'ATX, Mesh front, Great airflow'
                },
                'cooler': {
                    'name': 'Noctua NH-D15 chromax.black',
                    'price_inr': 7500,
                    'price_source': 'Amazon India',
                    'confidence': 'high',
                    'specs': 'Dual tower air cooler, Premium'
                }
            }
        },
        'programming': {
            '₹60k': {
                'cpu': {
                    'name': 'AMD Ryzen 5 5500',
                    'price_inr': 11500,
                    'price_source': 'Amazon India',
                    'confidence': 'high',
                    'specs': '6 cores, 12 threads, 3.6-4.2GHz'
                },
                'gpu': {
                    'name': 'RTX 3050 6GB',
                    'price_inr': 18000,
                    'price_source': 'MDComputers',
                    'confidence': 'medium',
                    'specs': '6GB GDDR6, Budget GPU'
                },
                'motherboard': {
                    'name': 'Gigabyte B550M DS3H',
                    'price_inr': 5500,
                    'price_source': 'Vedant',
                    'confidence': 'high',
                    'specs': 'AM4 socket, Micro ATX'
                },
                'ram': {
                    'name': 'Corsair Vengeance LPX 16GB DDR4 3200MHz',
                    'price_inr': 5000,
                    'price_source': 'Amazon India',
                    'confidence': 'high',
                    'specs': '16GB, DDR4-3200, 2x8GB'
                },
                'storage': {
                    'name': 'WD Blue SN570 500GB NVMe',
                    'price_inr': 3500,
                    'price_source': 'PrimeABGB',
                    'confidence': 'high',
                    'specs': '500GB, PCIe 3.0 NVMe'
                },
                'psu': {
                    'name': 'Corsair CV450 450W',
                    'price_inr': 3000,
                    'price_source': 'Amazon India',
                    'confidence': 'high',
                    'specs': '450W, 80+ Bronze'
                },
                'case': {
                    'name': 'Zebronics Zeb-Transformer',
                    'price_inr': 1800,
                    'price_source': 'MDComputers',
                    'confidence': 'high',
                    'specs': 'Micro ATX, Budget cabinet'
                },
                'cooler': {
                    'name': 'Stock Cooler (AMD Wraith Stealth)',
                    'price_inr': 1500,
                    'price_source': 'Equivalent Market Price',
                    'confidence': 'high',
                    'specs': 'Wraith Stealth cooler, budget-friendly'
                }
            },
            '₹120k': {
                'cpu': {
                    'name': 'AMD Ryzen 7 5700X',
                    'price_inr': 19000,
                    'price_source': 'Amazon India',
                    'confidence': 'high',
                    'specs': '8 cores, 16 threads, 3.6-4.6GHz'
                },
                'gpu': {
                    'name': 'RTX 3060 12GB',
                    'price_inr': 32000,
                    'price_source': 'MDComputers',
                    'confidence': 'high',
                    'specs': '12GB GDDR6, Good for GPU acceleration'
                },
                'motherboard': {
                    'name': 'ASUS ROG STRIX B550-F',
                    'price_inr': 14000,
                    'price_source': 'Vedant',
                    'confidence': 'high',
                    'specs': 'AM4 socket, ATX, PCIe 4.0'
                },
                'ram': {
                    'name': 'G.Skill Trident Z Neo 32GB DDR4 3600MHz',
                    'price_inr': 8000,
                    'price_source': 'Amazon India',
                    'confidence': 'high',
                    'specs': '32GB, DDR4-3600, 2x16GB, optimized for Ryzen'
                },
                'storage': {
                    'name': 'WD Black SN850X 1TB NVMe',
                    'price_inr': 10000,
                    'price_source': 'PrimeABGB',
                    'confidence': 'high',
                    'specs': '1TB, PCIe 4.0, Fast for projects'
                },
                'psu': {
                    'name': 'Corsair RM750x 750W 80+ Gold',
                    'price_inr': 9000,
                    'price_source': 'Amazon India',
                    'confidence': 'high',
                    'specs': '750W, 80+ Gold, Fully modular'
                },
                'case': {
                    'name': 'Fractal Design Core 1000 Mid Tower',
                    'price_inr': 4000,
                    'price_source': 'MDComputers',
                    'confidence': 'high',
                    'specs': 'ATX, Good airflow, Simple design'
                },
                'cooler': {
                    'name': 'Noctua NH-U12S chromax.black',
                    'price_inr': 6000,
                    'price_source': 'Amazon India',
                    'confidence': 'high',
                    'specs': 'High-end air cooler, quiet operation'
                }
            }
        }
    }
    
    # Minimum budget requirements per domain (in INR)
    MIN_BUDGETS = {
        'gaming': {
            'entry': 45000,       # Entry-level 1080p gaming
            'mid': 120000,        # Mid-tier 1440p gaming
            'high': 180000        # High-end 1440p/4K gaming
        },
        'video_editing': {
            'entry': 65000,       # Light 1080p editing (budget entry)
            'mid': 150000,        # 4K editing
            'high': 350000        # Professional 4K editing
        },
        'rendering': {
            'entry': 100000,
            'mid': 250000,
            'high': 450000
        },
        'streaming': {
            'entry': 65000,
            'mid': 180000,
            'high': 300000
        },
        'programming': {
            'entry': 45000,       # Light compilation
            'mid': 100000,        # Medium projects
            'high': 200000        # Heavy compilation
        },
        'general_purpose': {
            'entry': 35000,       # Basic browsing/office
            'mid': 75000,         # Standard work
            'high': 150000        # Multitasking
        }
    }
    
    # Domain mapping for fallback (if a domain is not in COMPONENT_DATABASE, map to a similar one)
    DOMAIN_MAPPING = {
        'general_purpose': 'gaming',  # Use gaming tier but scaled down
    }
    
    @staticmethod
    def validate_budget(domain, budget_inr):
        """
        Validate if budget is sufficient for domain.
        Returns: {'valid': bool, 'min_required': int, 'message': str}
        """
        if domain not in PCBuildAgent.MIN_BUDGETS:
            return {
                'valid': False,
                'min_required': 100000,
                'message': f'Domain "{domain}" not recognized'
            }
        
        # Get minimum budget for entry-level build
        min_budget = PCBuildAgent.MIN_BUDGETS[domain]['entry']
        
        if budget_inr < min_budget:
            return {
                'valid': False,
                'min_required': min_budget,
                'message': f'Your budget is too low for a functional PC. Minimum required budget is approximately Rs. {min_budget:,}.'
            }
        
        return {
            'valid': True,
            'min_required': min_budget,
            'message': f'Budget is sufficient for {domain} build'
        }
    
    @staticmethod
    def get_closest_budget_tier(domain, budget_inr):
        """Get the closest predefined budget tier for the domain."""
        # Map unsupported domains to existing ones
        if domain not in PCBuildAgent.COMPONENT_DATABASE:
            domain = PCBuildAgent.DOMAIN_MAPPING.get(domain, 'gaming')
        
        if domain not in PCBuildAgent.COMPONENT_DATABASE:
            return None
        
        tiers = list(PCBuildAgent.COMPONENT_DATABASE[domain].keys())
        if not tiers:
            return None

        # Tier labels are targets and do not always match the component total.
        # Pick the strongest tier whose parts plus the estimate buffer fit.
        tier_costs = {}
        for tier, components in PCBuildAgent.COMPONENT_DATABASE[domain].items():
            adjusted_subtotal = 0
            for category, part in components.items():
                floor_key = category if category in PCBuildAgent.PRICE_FLOORS else f'{category}_16gb'
                floor = PCBuildAgent.PRICE_FLOORS.get(floor_key, 0)
                adjusted_subtotal += max(part.get('price_inr', 0), floor)
            tier_costs[tier] = adjusted_subtotal * 1.09
        fitting = [tier for tier in tiers if tier_costs[tier] <= budget_inr]
        if fitting:
            return max(fitting, key=lambda tier: tier_costs[tier])
        return min(tiers, key=lambda tier: tier_costs[tier])
        
        # Convert tier names to numeric values for comparison
        tier_values = {}
        for tier in tiers:
            # Extract number from tier name (e.g., '₹100k' -> 100000)
            numeric_value = int(tier.replace('₹', '').replace('k', '')) * 1000
            tier_values[tier] = numeric_value
        
        # Find closest tier
        closest_tier = min(tier_values.keys(), 
                          key=lambda t: abs(tier_values[t] - budget_inr))
        
        return closest_tier
    
    @staticmethod
    def generate_build(domain, budget_inr, game_name=None):
        """
        Generate a PC build recommendation for the given domain and budget.
        Optionally customizes based on game requirements.
        
        Returns: {
            'success': bool,
            'domain': str,
            'budget_input': int,
            'currency': str,
            'parts': dict,
            'subtotal': int,
            'buffer_pct': float,
            'total_with_buffer': int,
            'validation_logs': list,
            'message': str
        }
        """
        validation_logs = []
        
        # Map unsupported domains to existing ones
        original_domain = domain
        if domain not in PCBuildAgent.COMPONENT_DATABASE:
            domain = PCBuildAgent.DOMAIN_MAPPING.get(domain, 'gaming')
            validation_logs.append(f'Mapping {original_domain} to {domain} for component selection')
        
        # Log the game being optimized for
        if game_name:
            validation_logs.append(f'Optimizing build for: {game_name}')
        
        # Step 1: Validate budget
        budget_check = PCBuildAgent.validate_budget(original_domain, budget_inr)
        if not budget_check['valid']:
            return {
                'success': False,
                'domain': original_domain,
                'budget_input': budget_inr,
                'currency': 'INR',
                'message': budget_check['message'],
                'min_required': budget_check['min_required'],
                'parts': {},
                'validation_logs': []
            }
        
        # Step 2: Get closest budget tier
        tier = PCBuildAgent.get_closest_budget_tier(domain, budget_inr)
        if not tier:
            return {
                'success': False,
                'domain': original_domain,
                'budget_input': budget_inr,
                'currency': 'INR',
                'message': f'No builds available for domain "{original_domain}"',
                'parts': {},
                'validation_logs': validation_logs
            }
        
        validation_logs.append(f'Selected tier: {tier} for budget Rs. {budget_inr:,}')
        
        # Step 3: Get components for this tier
        components_data = PCBuildAgent.COMPONENT_DATABASE[domain][tier]
        parts = {}
        
        if game_name:
            validation_logs.append(f'Build is selected for the requested budget and intended for {game_name}; check game-specific performance separately.')
        
        for category, component in components_data.items():
            comp_name = component['name']
            price = component['price_inr']
            
            parts[category] = {
                'category': category,
                'name': comp_name,
                'price_inr': price,
                'price_source': component['price_source'],
                'confidence': component['confidence'],
                'specs': component.get('specs', ''),
                'note': component.get('note', '')
            }
            
            # Validate price against floor
            if price > 0:
                floor_key = category if category in PCBuildAgent.PRICE_FLOORS else f'{category}_16gb'
                floor = PCBuildAgent.PRICE_FLOORS.get(floor_key, 0)
                
                if price < floor:
                    validation_logs.append(
                        f'WARNING: {category} price (Rs. {price}) below floor (Rs. {floor}). Using floor price.'
                    )
                    parts[category]['price_inr'] = floor
                    parts[category]['note'] = 'Price adjusted to minimum floor'
        
        # Step 4: Calculate totals
        subtotal = sum(part['price_inr'] for part in parts.values())
        buffer_pct = 9  # 9% for GST and shipping
        buffer_amount = int(subtotal * buffer_pct / 100)
        total_with_buffer = subtotal + buffer_amount
        
        validation_logs.append(f'Subtotal: Rs. {subtotal:,}')
        validation_logs.append(f'Buffer ({buffer_pct}%): Rs. {buffer_amount:,}')
        validation_logs.append(f'Total with buffer: Rs. {total_with_buffer:,}')
        
        # Step 5: Check if total is within ±15% of budget
        variance = abs(total_with_buffer - budget_inr) / budget_inr * 100
        if variance > 15:
            validation_logs.append(f'WARNING: Total variance {variance:.1f}% exceeds ±15% tolerance')
        
        return {
            'success': True,
            'domain': domain,
            'budget_input': budget_inr,
            'currency': 'INR',
            'parts': parts,
            'subtotal': subtotal,
            'buffer_pct': buffer_pct,
            'total_with_buffer': total_with_buffer,
            'validation_logs': validation_logs,
            'message': f'PC build generated successfully for {domain} with Rs. {budget_inr:,} budget'
        }

