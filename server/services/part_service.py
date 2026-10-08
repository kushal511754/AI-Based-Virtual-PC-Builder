"""Part service - fetch components from database."""
from server.utils.db import get_db_connection, dict_from_row

class PartService:
    @staticmethod
    def get_all_parts():
        """Get all parts organized by type."""
        return {
            'cpu': PartService.get_all_cpus(),
            'gpu': PartService.get_all_gpus(),
            'motherboard': PartService.get_all_motherboards(),
            'ram': PartService.get_all_ram(),
            'storage': PartService.get_all_storage(),
            'psu': PartService.get_all_psus(),
            'case': PartService.get_all_cases(),
            'cooling': PartService.get_all_cooling()
        }
    
    @staticmethod
    def get_all_cpus():
        """Get all CPUs."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cpu ORDER BY price ASC")
        cpus = [dict_from_row(row) for row in cursor.fetchall()]
        conn.close()
        return cpus
    
    @staticmethod
    def get_all_gpus():
        """Get all GPUs."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM gpu ORDER BY price ASC")
        gpus = [dict_from_row(row) for row in cursor.fetchall()]
        conn.close()
        return gpus
    
    @staticmethod
    def get_all_motherboards():
        """Get all motherboards."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM motherboard ORDER BY price ASC")
        motherboards = [dict_from_row(row) for row in cursor.fetchall()]
        conn.close()
        return motherboards
    
    @staticmethod
    def get_all_ram():
        """Get all RAM."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ram ORDER BY price ASC")
        ram = [dict_from_row(row) for row in cursor.fetchall()]
        conn.close()
        return ram
    
    @staticmethod
    def get_all_storage():
        """Get all storage devices."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM storage ORDER BY price ASC")
        storage = [dict_from_row(row) for row in cursor.fetchall()]
        conn.close()
        return storage
    
    @staticmethod
    def get_all_psus():
        """Get all power supplies."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM psu ORDER BY price ASC")
        psus = [dict_from_row(row) for row in cursor.fetchall()]
        conn.close()
        return psus
    
    @staticmethod
    def get_all_cases():
        """Get all cases."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pc_case ORDER BY price ASC")
        cases = [dict_from_row(row) for row in cursor.fetchall()]
        conn.close()
        return cases
    
    @staticmethod
    def get_all_cooling():
        """Get all cooling solutions."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cooling ORDER BY price ASC")
        cooling = [dict_from_row(row) for row in cursor.fetchall()]
        conn.close()
        return cooling
    
    @staticmethod
    def get_cpu_by_id(cpu_id):
        """Get CPU by ID."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cpu WHERE id = ?", (cpu_id,))
        cpu = dict_from_row(cursor.fetchone())
        conn.close()
        return cpu
    
    @staticmethod
    def get_motherboards_by_socket(socket_type):
        """Get motherboards compatible with socket."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM motherboard WHERE socket_type = ? ORDER BY price ASC", (socket_type,))
        motherboards = [dict_from_row(row) for row in cursor.fetchall()]
        conn.close()
        return motherboards
