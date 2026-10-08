"""API routes for global component search using real-time e-commerce data."""
from flask import Blueprint, request, jsonify
import logging

logger = logging.getLogger(__name__)

search_bp = Blueprint('search', __name__, url_prefix='/api/search')

def _get_realtime_fetcher():
    """Lazy load real-time component fetcher."""
    from server.services.realtime_component_fetcher import RealtimeComponentFetcher
    return RealtimeComponentFetcher()

def _get_ai_search():
    """Lazy load AI search service (fallback)."""
    from server.services.ai_component_search import AIComponentSearch
    return AIComponentSearch()

@search_bp.route('/component', methods=['POST'])
def search_component():
    """
    Search for a PC component using real-time e-commerce pricing.
    
    Request body:
    {
        "query": "AMD Ryzen 7 5800X3D",
        "component_type": "cpu"  (optional, auto-detect if not provided)
    }
    """
    try:
        data = request.get_json() or {}
        query = data.get('query', '').strip()
        component_type = data.get('component_type', '').strip().lower()
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'Query parameter is required'
            }), 400
        
        # Component type detection if not provided
        component_types = ['cpu', 'gpu', 'motherboard', 'ram', 'storage', 'psu', 'case', 'cooling', 'ssd', 'hdd', 'monitor', 'keyboard', 'mouse', 'headphones', 'mousepad']
        
        if not component_type:
            # Try to auto-detect from query
            query_lower = query.lower()
            if any(word in query_lower for word in ['ryzen', 'core i', 'cpu', 'processor', 'xeon', 'pentium', 'i9', 'i7', 'i5']):
                component_type = 'cpu'
            elif any(word in query_lower for word in ['gpu', 'graphics', 'rtx', 'geforce', 'radeon', 'rx 7', '4070', '4090', '4080', '4060', '3070', '3080']):
                component_type = 'gpu'
            elif any(word in query_lower for word in ['motherboard', 'mobo', 'b550', 'z790', 'x870', 'b850', 'b450', 'tomahawk', 'asus rog', 'msi mpg']):
                component_type = 'motherboard'
            elif any(word in query_lower for word in ['ram', 'memory', 'ddr4', 'ddr5', 'corsair vengeance', 'trident', 'g.skill', 'kingston fury']):
                component_type = 'ram'
            elif any(word in query_lower for word in ['ssd', 'nvme', 'samsung 980', 'wd black', 'crucial', 'kingston fury beast']):
                component_type = 'ssd'
            elif any(word in query_lower for word in ['hdd', 'seagate', 'wd blue']):
                component_type = 'hdd'
            elif any(word in query_lower for word in ['storage', 'disk']):
                component_type = 'storage'
            elif any(word in query_lower for word in ['psu', 'power supply', '650w', '750w', '850w', '1000w', 'corsair rm', 'evga', 'seasonic']):
                component_type = 'psu'
            elif any(word in query_lower for word in ['case', 'tower', 'chassis', 'nzxt', 'corsair 4000', 'lian li', 'fractal']):
                component_type = 'case'
            elif any(word in query_lower for word in ['cooler', 'cooling', 'fan', 'liquid', 'hyper 212', 'noctua', 'kraken', 'dark rock']):
                component_type = 'cooling'
            elif any(word in query_lower for word in ['monitor', 'display', 'screen', 'lcd', 'oled', 'curved', 'dell', 'asus vp', 'lg', '1080p', '1440p', '4k']):
                component_type = 'monitor'
            elif any(word in query_lower for word in ['keyboard', 'kbd', 'mechanical', 'corsair k', 'logitech g', 'steelseries', 'razer']):
                component_type = 'keyboard'
            elif any(word in query_lower for word in ['mouse', 'g pro', 'superlight', 'dark core', 'rival', 'deathadder', 'logitech g']):
                component_type = 'mouse'
            elif any(word in query_lower for word in ['headphones', 'headset', 'arctis', 'virtuoso', 'cloud stinger', 'blackshark', 'gaming audio']):
                component_type = 'headphones'
            elif any(word in query_lower for word in ['mousepad', 'mouse pad', 'qck', 'mm1000', 'g740']):
                component_type = 'mousepad'
            else:
                component_type = 'cpu'  # Default
        
        if component_type not in component_types:
            return jsonify({
                'success': False,
                'error': f'Invalid component type: {component_type}'
            }), 400
        
        # Try real-time fetcher first (live pricing from e-commerce platforms)
        realtime_fetcher = _get_realtime_fetcher()
        result = realtime_fetcher.search_component(query, component_type)
        
        # Fallback to AI search if real-time fails
        if not result.get('success'):
            ai_search = _get_ai_search()
            result = ai_search.search_component(query, component_type)
        
        return jsonify(result), 200 if result.get('success') else 400
        
    except Exception as e:
        logger.error(f"Error in search_component: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@search_bp.route('/all', methods=['POST'])
def search_all_types():
    """
    Search component across all types.
    
    Request body:
    {
        "query": "AMD Ryzen 7 5800X3D",
        "limit": 5
    }
    """
    try:
        data = request.json or {}
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'Query parameter is required'
            }), 400
        
        ai_search = _get_ai_search()
        components = ai_search.search_multiple(query)
        
        return jsonify({
            'success': True,
            'components': components,
            'count': len(components)
        }), 200
        
    except Exception as e:
        logger.error(f"Error in search_all_types: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
