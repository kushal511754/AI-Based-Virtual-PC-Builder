"""Builder API routes."""
from flask import Blueprint, jsonify, request
import logging

logger = logging.getLogger(__name__)

builder_bp = Blueprint('builder', __name__, url_prefix='/api/builder')

# Lazy imports to avoid loading heavy services at startup
def _get_part_service():
    from server.services.part_service import PartService
    return PartService()

def _get_compatibility_engine():
    from server.services.compatibility_engine import CompatibilityEngine
    return CompatibilityEngine()

def _get_pricing_service():
    from server.services.pricing_service import PricingService
    return PricingService()

def _get_build_service():
    from server.services.build_service import BuildService
    return BuildService()

@builder_bp.route('/parts', methods=['GET'])
def get_all_parts():
    """Get all available parts for manual building."""
    try:
        service = _get_part_service()
        parts = service.get_all_parts()
        
        return jsonify({
            'success': True,
            'parts': parts
        }), 200
    except Exception as e:
        logger.error(f"Error in get_all_parts: {e}", exc_info=True)
        return jsonify({'error': str(e), 'success': False}), 500

@builder_bp.route('/validate', methods=['POST'])
def validate_build():
    """Validate PC build compatibility."""
    try:
        engine = _get_compatibility_engine()
        data = request.json or {}
        result = engine.validate_build(
            cpu_id=data.get('cpu_id'),
            motherboard_id=data.get('motherboard_id'),
            gpu_id=data.get('gpu_id'),
            psu_id=data.get('psu_id'),
            case_id=data.get('case_id'),
            ram_id=data.get('ram_id'),
            cooling_id=data.get('cooling_id')
        )
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error in validate_build: {e}", exc_info=True)
        return jsonify({'error': str(e), 'success': False}), 500

@builder_bp.route('/price', methods=['POST'])
def price_build():
    """Analyze build pricing."""
    try:
        service = _get_pricing_service()
        data = request.json or {}
        result = service.analyze_build(
            cpu_id=data.get('cpu_id'),
            motherboard_id=data.get('motherboard_id'),
            gpu_id=data.get('gpu_id'),
            psu_id=data.get('psu_id'),
            case_id=data.get('case_id'),
            ram_id=data.get('ram_id'),
            storage_id=data.get('storage_id'),
            cooling_id=data.get('cooling_id')
        )
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error in price_build: {e}", exc_info=True)
        return jsonify({'error': str(e), 'success': False}), 500

@builder_bp.route('/save', methods=['POST'])
def save_build():
    """Save a PC build."""
    try:
        data = request.json or {}
        
        build_id = BuildService.save_build(
            build_name=data.get('build_name', 'Unnamed Build'),
            cpu_id=None,
            gpu_id=None,
            motherboard_id=None,
            ram_id=None,
            storage_id=None,
            psu_id=None,
            case_id=None,
            cooling_id=None,
            total_price=data.get('total_price', 0)
        )
        
        return jsonify({'success': True, 'build_id': build_id}), 200
    except Exception as e:
        logger.error(f"Error in save_build: {e}", exc_info=True)
        return jsonify({'error': str(e), 'success': False}), 500

@builder_bp.route('/save-build', methods=['POST'])
def save_ai_build():
    """Save an AI-generated PC build (handles both AI and manual builds)."""
    try:
        data = request.json or {}
        import json
        
        # Handle both AI format (suggested_parts) and manual format (direct properties)
        suggested_parts = data.get('suggested_parts')
        if not suggested_parts:
            # Convert manual format to suggested_parts
            suggested_parts = {
                'cpu': data.get('cpu'),
                'gpu': data.get('gpu'),
                'motherboard': data.get('motherboard'),
                'ram': data.get('ram'),
                'storage': data.get('storage'),
                'psu': data.get('psu'),
                'case': data.get('case'),
                'cooling': data.get('cooling')
            }
        
        # Extract build data
        build_name = data.get('build_name') or data.get('domain', 'Gaming') + ' Build'
        total_price = data.get('total_price', 0)
        domain = data.get('domain', 'General')
        game_name = data.get('game_name', '')
        
        # Store the complete build architecture with all details
        build_architecture = {
            'domain': domain,
            'game_name': game_name,
            'total_price': total_price,
            'budget': data.get('budget', 0),
            'message': data.get('message', ''),
            'compatibility': data.get('compatibility', {}),
            'components': suggested_parts  # Full component objects with specs and prices
        }
        
        # For AI builds, we'll store the entire build with no component IDs
        # since AI builds don't have database component IDs
        service = _get_build_service()
        build_id = service.save_build(
            build_name=build_name,
            cpu_id=None,
            gpu_id=None,
            motherboard_id=None,
            ram_id=None,
            storage_id=None,
            psu_id=None,
            case_id=None,
            cooling_id=None,
            total_price=total_price,
            suggested_parts=json.dumps(build_architecture),
            domain=domain,
            game_name=game_name
        )
        
        return jsonify({
            'success': True,
            'build_id': build_id,
            'message': f'Build saved successfully! (ID: {build_id})'
        }), 200
    except Exception as e:
        logger.error(f"Error in save_ai_build: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': f'Error saving build: {str(e)}'
        }), 500

@builder_bp.route('/builds', methods=['GET'])
def get_builds():
    """Get all saved builds."""
    try:
        service = _get_build_service()
        builds = service.get_all_builds()
        return jsonify(builds), 200
    except Exception as e:
        logger.error(f"Error in get_builds: {e}", exc_info=True)
        return jsonify({'error': str(e), 'success': False}), 500

@builder_bp.route('/build/<int:build_id>', methods=['GET'])
def get_build(build_id):
    """Get a specific build with full details."""
    try:
        service = _get_build_service()
        build_details = service.get_build_details(build_id)
        if not build_details:
            return jsonify({'error': 'Build not found', 'success': False}), 404
        return jsonify(build_details), 200
    except Exception as e:
        logger.error(f"Error in get_build: {e}", exc_info=True)
        return jsonify({'error': str(e), 'success': False}), 500

@builder_bp.route('/build/<int:build_id>', methods=['DELETE'])
def delete_build(build_id):
    """Delete a saved build."""
    try:
        service = _get_build_service()
        service.delete_build(build_id)
        return jsonify({'success': True}), 200
    except Exception as e:
        logger.error(f"Error in delete_build: {e}", exc_info=True)
        return jsonify({'error': str(e), 'success': False}), 500

@builder_bp.route('/recommend/<component_type>', methods=['POST'])
def recommend_component(component_type):
    """Get recommended components based on current build compatibility."""
    try:
        data = request.json or {}
        engine = _get_compatibility_engine()
        service = _get_part_service()
        
        # Get all components of this type based on the type parameter
        type_map = {
            'cpu': 'all_cpus',
            'gpu': 'all_gpus',
            'motherboard': 'all_motherboards',
            'ram': 'all_ram',
            'storage': 'all_storage',
            'psu': 'all_psus',
            'case': 'all_cases',
            'cooling': 'all_cooling'
        }
        
        method_name = type_map.get(component_type)
        if not method_name:
            return jsonify({'success': True, 'recommended_ids': []}), 200
        
        # Get all components of this type
        method = getattr(service, method_name)
        all_components = method()
        
        if not all_components:
            return jsonify({'success': True, 'recommended_ids': []}), 200
        
        # Score each component for compatibility
        recommended_ids = []
        scored_components = []
        
        # Get the CPU if present for power calculations
        cpu_name = data.get('cpu', '')
        cpu = None
        if cpu_name:
            all_cpus = service.get_all_cpus()
            cpu = next((c for c in all_cpus if c.get('name', '').lower() == cpu_name.lower()), None)
        
        for component in all_components:
            # Calculate compatibility score
            score = 50  # Base score
            
            try:
                # Check RAM compatibility with motherboard
                if component_type == 'ram' and data.get('motherboard'):
                    all_mbs = service.get_all_motherboards()
                    mb = next((m for m in all_mbs if m.get('name', '').lower() == data.get('motherboard', '').lower()), None)
                    if mb and component.get('type') == mb.get('ram_type'):
                        score = 100
                    elif mb and component.get('size_gb', 0) <= mb.get('max_ram_gb', 64):
                        score = 85
                
                # Check GPU/PSU compatibility
                elif component_type == 'psu' and data.get('gpu'):
                    all_gpus = service.get_all_gpus()
                    gpu = next((g for g in all_gpus if g.get('name', '').lower() == data.get('gpu', '').lower()), None)
                    if gpu and cpu:
                        required_power = cpu.get('tdp', 0) + gpu.get('power_draw', 0) + 150
                        psu_wattage = component.get('wattage', 0)
                        if required_power <= psu_wattage * 0.8:
                            score = 100
                        elif required_power <= psu_wattage:
                            score = 85
                        else:
                            score = 0
                
                # Check CPU socket with motherboard
                elif component_type == 'cpu' and data.get('motherboard'):
                    all_mbs = service.get_all_motherboards()
                    mb = next((m for m in all_mbs if m.get('name', '').lower() == data.get('motherboard', '').lower()), None)
                    if mb and component.get('socket_type') == mb.get('socket_type'):
                        score = 100
                
                # Check motherboard socket with CPU
                elif component_type == 'motherboard' and data.get('cpu'):
                    all_cpus = service.get_all_cpus()
                    cpu = next((c for c in all_cpus if c.get('name', '').lower() == data.get('cpu', '').lower()), None)
                    if cpu and component.get('socket_type') == cpu.get('socket_type'):
                        score = 100
            except Exception as score_err:
                logger.warning(f"Error calculating score for component: {score_err}")
                score = 50
            
            if score > 0:
                scored_components.append({
                    'id': component.get('id'),
                    'score': score
                })
        
        # Sort by score and get top 5
        scored_components.sort(key=lambda x: x['score'], reverse=True)
        recommended_ids = [c['id'] for c in scored_components[:5]]
        
        return jsonify({
            'success': True,
            'recommended_ids': recommended_ids
        }), 200
    except Exception as e:
        logger.error(f"Error in recommend_component: {e}", exc_info=True)
        return jsonify({
            'success': True,
            'recommended_ids': []
        }), 200
