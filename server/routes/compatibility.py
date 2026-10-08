from flask import Blueprint, request, jsonify
from server.services.component_compatibility import ComponentCompatibility
from server.services.compatibility_engine import CompatibilityEngine
from server.utils.db import get_db_connection, dict_from_row
import logging

logger = logging.getLogger(__name__)

compatibility_bp = Blueprint('compatibility', __name__, url_prefix='/api/builder')

@compatibility_bp.route('/compatibility', methods=['POST'])
def check_compatibility():
    """Check compatibility between selected components"""
    try:
        data = request.json or {}
        compatibility = ComponentCompatibility()
        
        result = compatibility.analyze(data)
        
        return jsonify({
            'success': True,
            'issues': result.get('issues', []),
            'warnings': result.get('warnings', []),
            'details': result.get('details', ''),
            'overall_score': result.get('overall_score', 0)
        })
    except Exception as e:
        logger.error(f"Compatibility check error: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e),
            'issues': [],
            'warnings': []
        }), 500

@compatibility_bp.route('/check', methods=['POST'])
def check_build_compatibility():
    """Real-time compatibility check for manual PC builder with smart suggestions"""
    return jsonify({'status': 'ok', 'compatible': False, 'errors': ['test'], 'suggestions': []})


def get_compatibility_suggestions(build_data, compat_result):
    """Generate smart suggestions for incompatible parts"""
    from server.utils.db import get_db_connection, dict_from_row
    
    suggestions = []
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check for CPU-Motherboard socket issues
        if 'Socket Mismatch' in str(compat_result.get('errors', [])):
            cpu_id = build_data.get('cpu')
            
            if cpu_id:
                # Get current CPU socket
                cursor.execute("SELECT socket_type FROM cpu WHERE id = ?", (cpu_id,))
                cpu_row = cursor.fetchone()
                if cpu_row:
                    current_socket = dict_from_row(cpu_row)['socket_type']
                    
                    # Find compatible motherboards
                    cursor.execute(
                        "SELECT id, name, price FROM motherboard WHERE socket_type = ? ORDER BY price ASC LIMIT 3",
                        (current_socket,)
                    )
                    
                    for row in cursor.fetchall():
                        mb = dict_from_row(row)
                        suggestions.append({
                            'type': 'motherboard',
                            'name': mb['name'],
                            'id': mb['id'],
                            'price': round(mb['price'] * 83, 2)
                        })
        
        # Check for RAM type issues
        if any('RAM Type Mismatch' in str(err) for err in compat_result.get('errors', [])):
            mb_id = build_data.get('motherboard')
            
            if mb_id:
                # Get motherboard RAM type
                cursor.execute("SELECT ram_type FROM motherboard WHERE id = ?", (mb_id,))
                mb_row = cursor.fetchone()
                if mb_row:
                    ram_type = dict_from_row(mb_row)['ram_type']
                    
                    # Find compatible RAM
                    cursor.execute(
                        "SELECT id, name, price FROM ram WHERE type = ? ORDER BY price ASC LIMIT 3",
                        (ram_type,)
                    )
                    
                    for row in cursor.fetchall():
                        ram = dict_from_row(row)
                        suggestions.append({
                            'type': 'ram',
                            'name': ram['name'],
                            'id': ram['id'],
                            'price': round(ram['price'] * 83, 2)
                        })
        
        # Check for PSU power issues
        if any('Insufficient PSU' in str(err) for err in compat_result.get('errors', [])):
            # Find higher wattage PSUs
            cursor.execute(
                "SELECT id, name, wattage, price FROM psu ORDER BY wattage DESC, price ASC LIMIT 3"
            )
            
            for row in cursor.fetchall():
                psu = dict_from_row(row)
                suggestions.append({
                    'type': 'psu',
                    'name': f"{psu['name']} ({psu['wattage']}W)",
                    'id': psu['id'],
                    'price': round(psu['price'] * 83, 2)
                })
        
        # Check for GPU size issues
        if any('GPU Too Long' in str(err) for err in compat_result.get('errors', [])):
            case_id = build_data.get('case')
            
            if case_id:
                cursor.execute("SELECT max_gpu_length_mm FROM pc_case WHERE id = ?", (case_id,))
                case_row = cursor.fetchone()
                if case_row:
                    max_length = dict_from_row(case_row)['max_gpu_length_mm']
                    
                    # Find smaller GPUs
                    cursor.execute(
                        "SELECT id, name, length_mm, price FROM gpu WHERE length_mm <= ? ORDER BY length_mm DESC, price DESC LIMIT 3",
                        (max_length,)
                    )
                    
                    for row in cursor.fetchall():
                        gpu = dict_from_row(row)
                        suggestions.append({
                            'type': 'gpu',
                            'name': gpu['name'],
                            'id': gpu['id'],
                            'price': round(gpu['price'] * 83, 2)
                        })
        
        conn.close()
    except Exception as e:
        logger.error(f"Error generating suggestions: {e}", exc_info=True)
    
    return suggestions
