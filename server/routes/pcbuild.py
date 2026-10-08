"""
API routes for PCBuildAgent - Indian market PC builds in INR.
"""

from flask import Blueprint, request, jsonify
from server.services.pc_build_agent import PCBuildAgent

pcbuild_bp = Blueprint('pcbuild', __name__, url_prefix='/api/pcbuild')

@pcbuild_bp.route('/build', methods=['POST'])
def generate_build():
    """
    Generate a PC build recommendation for Indian market in INR.
    
    Request body:
    {
        "domain": "gaming" | "video_editing" | "rendering" | "streaming",
        "budget": <int in INR>
    }
    
    Response:
    {
        "success": bool,
        "domain": str,
        "budget_input": int,
        "currency": "INR",
        "parts": {...},
        "subtotal": int,
        "buffer_pct": float,
        "total_with_buffer": int,
        "validation_logs": [...],
        "message": str
    }
    """
    try:
        data = request.get_json()
        domain = data.get('domain', '').lower()
        budget = data.get('budget', 0)
        
        # Validate input
        if not domain or budget <= 0:
            return jsonify({
                'success': False,
                'message': 'Invalid domain or budget. Please provide valid values.'
            }), 400
        
        # Generate build using PCBuildAgent
        result = PCBuildAgent.generate_build(domain, budget)
        
        return jsonify(result), 200 if result['success'] else 400
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error generating build: {str(e)}'
        }), 500

@pcbuild_bp.route('/validate-budget', methods=['POST'])
def validate_budget():
    """
    Validate if budget is sufficient for domain.
    
    Request body:
    {
        "domain": str,
        "budget": int in INR
    }
    """
    try:
        data = request.get_json()
        domain = data.get('domain', '').lower()
        budget = data.get('budget', 0)
        
        result = PCBuildAgent.validate_budget(domain, budget)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error validating budget: {str(e)}'
        }), 500

@pcbuild_bp.route('/domains', methods=['GET'])
def get_domains():
    """Get available domains and their minimum budgets."""
    try:
        domains = []
        for domain, budgets in PCBuildAgent.MIN_BUDGETS.items():
            domains.append({
                'name': domain,
                'display_name': domain.replace('_', ' ').title(),
                'min_budget': budgets['entry'],
                'recommended_budget': budgets['mid'],
                'premium_budget': budgets['high']
            })
        
        return jsonify({
            'success': True,
            'domains': domains
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching domains: {str(e)}'
        }), 500

