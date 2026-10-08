"""Compatibility checking engine."""
from server.utils.db import get_db_connection, dict_from_row

class CompatibilityEngine:
    def __init__(self):
        self.warnings = []
        self.errors = []
        self.compatible = True
    
    def validate_build(self, cpu_id, motherboard_id, gpu_id, psu_id, case_id, ram_id, cooling_id):
        """Validate entire build compatibility."""
        self.warnings = []
        self.errors = []
        self.compatible = True
        
        if not cpu_id or not motherboard_id:
            self.errors.append("CPU and Motherboard are required")
            self.compatible = False
            return {
                'compatible': self.compatible,
                'errors': self.errors,
                'warnings': self.warnings
            }
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Fetch components
        cursor.execute("SELECT * FROM cpu WHERE id = ?", (cpu_id,))
        cpu = dict_from_row(cursor.fetchone())
        
        cursor.execute("SELECT * FROM motherboard WHERE id = ?", (motherboard_id,))
        motherboard = dict_from_row(cursor.fetchone())
        
        cursor.execute("SELECT * FROM gpu WHERE id = ?", (gpu_id,))
        gpu = dict_from_row(cursor.fetchone())
        
        cursor.execute("SELECT * FROM psu WHERE id = ?", (psu_id,))
        psu = dict_from_row(cursor.fetchone())
        
        cursor.execute("SELECT * FROM pc_case WHERE id = ?", (case_id,))
        case = dict_from_row(cursor.fetchone())
        
        cursor.execute("SELECT * FROM ram WHERE id = ?", (ram_id,))
        ram = dict_from_row(cursor.fetchone())
        
        cursor.execute("SELECT * FROM cooling WHERE id = ?", (cooling_id,))
        cooling = dict_from_row(cursor.fetchone())
        
        conn.close()
        
        # CPU ↔ Motherboard Socket Check
        if cpu and motherboard:
            self._check_socket_compatibility(cpu, motherboard)
        
        # RAM ↔ Motherboard Check
        if ram and motherboard:
            self._check_ram_compatibility(ram, motherboard)
        
        # GPU ↔ PSU Check
        if gpu and psu and cpu:
            self._check_power_compatibility(cpu, gpu, psu)
        
        # GPU ↔ Case Check
        if gpu and case:
            self._check_case_compatibility(gpu, case)
        
        # Case ↔ PSU Check
        if case and psu:
            self._check_case_psu_compatibility(case, psu)
        
        # Cooling ↔ CPU Check
        if cooling and cpu:
            self._check_cooling_compatibility(cooling, cpu)
        
        return {
            'compatible': self.compatible,
            'errors': self.errors,
            'warnings': self.warnings
        }
    
    def _check_socket_compatibility(self, cpu, motherboard):
        """Check if CPU socket matches motherboard socket."""
        if cpu['socket_type'] != motherboard['socket_type']:
            self.errors.append(f"Socket Mismatch: CPU uses {cpu['socket_type']} but Motherboard uses {motherboard['socket_type']}")
            self.compatible = False
    
    def _check_ram_compatibility(self, ram, motherboard):
        """Check if RAM type matches motherboard."""
        if ram['type'] != motherboard['ram_type']:
            self.errors.append(f"RAM Type Mismatch: RAM is {ram['type']} but Motherboard supports {motherboard['ram_type']}")
            self.compatible = False
        
        if ram['size_gb'] > motherboard['max_ram_gb']:
            self.errors.append(f"RAM Capacity Exceeded: {ram['size_gb']}GB exceeds max {motherboard['max_ram_gb']}GB")
            self.compatible = False
    
    def _check_power_compatibility(self, cpu, gpu, psu):
        """Check if PSU has enough power."""
        required_power = cpu['tdp'] + gpu['power_draw'] + 150  # 150W overhead
        
        if required_power > psu['wattage']:
            self.errors.append(f"Insufficient PSU: {required_power}W required, {psu['wattage']}W available")
            self.compatible = False
        elif required_power > psu['wattage'] * 0.8:
            self.warnings.append(f"PSU near max capacity: {required_power}W of {psu['wattage']}W (80% threshold)")
    
    def _check_case_compatibility(self, gpu, case):
        """Check if GPU fits in case."""
        if gpu['length_mm'] > case['max_gpu_length_mm']:
            self.errors.append(f"GPU Too Long: {gpu['length_mm']}mm exceeds case limit {case['max_gpu_length_mm']}mm")
            self.compatible = False
    
    def _check_case_psu_compatibility(self, case, psu):
        """Check if PSU fits in case."""
        if psu['wattage'] > case['max_psu_wattage']:
            self.warnings.append(f"PSU wattage {psu['wattage']}W exceeds case limit {case['max_psu_wattage']}W (may not fit)")
    
    def _check_cooling_compatibility(self, cooling, cpu):
        """Check if cooling solution can handle CPU TDP."""
        if cooling['socket_type'] != cpu['socket_type']:
            self.warnings.append(f"Cooling socket {cooling['socket_type']} may not be compatible with CPU socket {cpu['socket_type']}")
        
        if cooling['tdp_rating'] < cpu['tdp']:
            self.warnings.append(f"Cooling TDP {cooling['tdp_rating']}W is below CPU TDP {cpu['tdp']}W (may be inadequate)")
