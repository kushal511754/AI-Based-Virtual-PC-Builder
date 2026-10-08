"""Build service - save and load builds."""
from server.utils.db import get_db_connection, dict_from_row
from datetime import datetime

class BuildService:
    @staticmethod
    def save_build(build_name, cpu_id, gpu_id, motherboard_id, ram_id, storage_id, psu_id, case_id, cooling_id, total_price, suggested_parts=None, domain=None, game_name=None):
        """Save a PC build to database."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO saved_build 
            (build_name, cpu_id, gpu_id, motherboard_id, ram_id, storage_id, psu_id, case_id, cooling_id, total_price, suggested_parts, domain, game_name)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (build_name, cpu_id, gpu_id, motherboard_id, ram_id, storage_id, psu_id, case_id, cooling_id, total_price, suggested_parts, domain, game_name))
        
        conn.commit()
        build_id = cursor.lastrowid
        conn.close()
        
        return build_id
    
    @staticmethod
    def get_all_builds():
        """Get all saved builds."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM saved_build ORDER BY created_at DESC")
        builds = [dict_from_row(row) for row in cursor.fetchall()]
        conn.close()
        return builds
    
    @staticmethod
    def get_build_by_id(build_id):
        """Get a specific build."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM saved_build WHERE id = ?", (build_id,))
        build = dict_from_row(cursor.fetchone())
        conn.close()
        return build
    
    @staticmethod
    def get_build_details(build_id):
        """Get full build details with all components."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM saved_build WHERE id = ?", (build_id,))
        build = dict_from_row(cursor.fetchone())
        
        if not build:
            conn.close()
            return None
        
        details = {'build': build, 'components': {}}
        
        # Fetch all components
        if build['cpu_id']:
            cursor.execute("SELECT * FROM cpu WHERE id = ?", (build['cpu_id'],))
            details['components']['cpu'] = dict_from_row(cursor.fetchone())
        
        if build['gpu_id']:
            cursor.execute("SELECT * FROM gpu WHERE id = ?", (build['gpu_id'],))
            details['components']['gpu'] = dict_from_row(cursor.fetchone())
        
        if build['motherboard_id']:
            cursor.execute("SELECT * FROM motherboard WHERE id = ?", (build['motherboard_id'],))
            details['components']['motherboard'] = dict_from_row(cursor.fetchone())
        
        if build['ram_id']:
            cursor.execute("SELECT * FROM ram WHERE id = ?", (build['ram_id'],))
            details['components']['ram'] = dict_from_row(cursor.fetchone())
        
        if build['storage_id']:
            cursor.execute("SELECT * FROM storage WHERE id = ?", (build['storage_id'],))
            details['components']['storage'] = dict_from_row(cursor.fetchone())
        
        if build['psu_id']:
            cursor.execute("SELECT * FROM psu WHERE id = ?", (build['psu_id'],))
            details['components']['psu'] = dict_from_row(cursor.fetchone())
        
        if build['case_id']:
            cursor.execute("SELECT * FROM pc_case WHERE id = ?", (build['case_id'],))
            details['components']['case'] = dict_from_row(cursor.fetchone())
        
        if build['cooling_id']:
            cursor.execute("SELECT * FROM cooling WHERE id = ?", (build['cooling_id'],))
            details['components']['cooling'] = dict_from_row(cursor.fetchone())
        
        conn.close()
        return details
    
    @staticmethod
    def delete_build(build_id):
        """Delete a saved build."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM saved_build WHERE id = ?", (build_id,))
        conn.commit()
        conn.close()
