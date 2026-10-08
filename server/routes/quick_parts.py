"""
API routes for getting quick add parts by domain.
"""

from flask import Blueprint, jsonify
from server.services.pc_build_agent import PCBuildAgent

quick_parts_bp = Blueprint('quick_parts', __name__, url_prefix='/api/quick-parts')

@quick_parts_bp.route('/by-domain/<domain>', methods=['GET'])
def get_quick_parts_by_domain(domain):
    """Get quick add parts for a specific domain."""
    
    # Get the mid-tier build for the domain which should have all parts
    result = PCBuildAgent.generate_build(domain, 150000)  # Use a reasonable mid-tier budget
    
    if not result['success']:
        return jsonify({
            'success': False,
            'message': f'Could not generate quick parts for domain: {domain}',
            'parts': []
        }), 400
    
    parts = result.get('parts', {})
    quick_parts = []
    
    part_order = ['cpu', 'gpu', 'motherboard', 'ram', 'storage', 'psu', 'case', 'cooler']
    
    for part_type in part_order:
        if part_type in parts:
            part_data = parts[part_type]
            # Map 'cooler' to 'cooling' for frontend compatibility
            frontend_type = 'cooling' if part_type == 'cooler' else part_type
            quick_parts.append({
                'type': frontend_type,
                'name': part_data.get('name', ''),
                'price': part_data.get('price_inr', 0),
                'specs': part_data.get('specs', ''),
                'price_source': part_data.get('price_source', 'PCBuild Agent'),
                'category': part_type.upper()
            })
    
    return jsonify({
        'success': True,
        'domain': domain,
        'parts': quick_parts,
        'count': len(quick_parts)
    })
