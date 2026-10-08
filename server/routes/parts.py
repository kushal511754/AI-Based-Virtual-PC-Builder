"""Parts API routes."""
from flask import Blueprint, jsonify, request

parts_bp = Blueprint('parts', __name__, url_prefix='/api/parts')

# Lazy import
def _get_part_service():
    from server.services.part_service import PartService
    return PartService

@parts_bp.route('/cpu', methods=['GET'])
def get_cpus():
    """Get all CPUs."""
    try:
        PartService = _get_part_service()
        cpus = PartService.get_all_cpus()
        return jsonify(cpus), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@parts_bp.route('/gpu', methods=['GET'])
def get_gpus():
    """Get all GPUs."""
    try:
        PartService = _get_part_service()
        gpus = PartService.get_all_gpus()
        return jsonify(gpus), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@parts_bp.route('/motherboard', methods=['GET'])
def get_motherboards():
    """Get all motherboards."""
    try:
        PartService = _get_part_service()
        motherboards = PartService.get_all_motherboards()
        return jsonify(motherboards), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@parts_bp.route('/ram', methods=['GET'])
def get_ram():
    """Get all RAM."""
    try:
        PartService = _get_part_service()
        ram = PartService.get_all_ram()
        return jsonify(ram), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@parts_bp.route('/storage', methods=['GET'])
def get_storage():
    """Get all storage."""
    try:
        PartService = _get_part_service()
        storage = PartService.get_all_storage()
        return jsonify(storage), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@parts_bp.route('/psu', methods=['GET'])
def get_psus():
    """Get all power supplies."""
    try:
        PartService = _get_part_service()
        psus = PartService.get_all_psus()
        return jsonify(psus), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@parts_bp.route('/case', methods=['GET'])
def get_cases():
    """Get all cases."""
    try:
        PartService = _get_part_service()
        cases = PartService.get_all_cases()
        return jsonify(cases), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@parts_bp.route('/cooling', methods=['GET'])
def get_cooling():
    """Get all cooling solutions."""
    try:
        PartService = _get_part_service()
        cooling = PartService.get_all_cooling()
        return jsonify(cooling), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@parts_bp.route('/cpu/<int:cpu_id>/compatible-motherboards', methods=['GET'])
def get_compatible_motherboards(cpu_id):
    """Get motherboards compatible with CPU socket."""
    try:
        PartService = _get_part_service()
        cpu = PartService.get_cpu_by_id(cpu_id)
        if not cpu:
            return jsonify({'error': 'CPU not found'}), 404
        
        motherboards = PartService.get_motherboards_by_socket(cpu['socket_type'])
        return jsonify(motherboards), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@parts_bp.route('/search', methods=['GET'])
def search_parts():
    """Global search for any PC component with fuzzy matching - real-time from multiple sources."""
    try:
        from server.services.global_parts_service import GlobalPartsService
        
        query = request.args.get('q', '').lower().strip()
        part_type = request.args.get('type', '').lower()  # Optional: filter by type
        limit = request.args.get('limit', 100, type=int)
        
        if not query or len(query) < 2:
            return jsonify({'error': 'Query must be at least 2 characters'}), 400
        
        # Use global parts service for comprehensive search
        results = GlobalPartsService.search_global(query, part_type, limit)
        
        return jsonify({
            'success': True,
            'query': query,
            'count': len(results),
            'results': results
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
