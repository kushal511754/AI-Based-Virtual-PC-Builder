import re

class ComponentCompatibility:
    """Analyzes compatibility between PC components"""
    
    # Socket compatibility mappings
    SOCKET_MAPPINGS = {
        # Intel
        'i7': {'LGA1700': True, 'LGA1200': False},
        'i5': {'LGA1700': True, 'LGA1200': True},
        'i3': {'LGA1700': True, 'LGA1200': True},
        'core i7': {'LGA1700': True, 'LGA1200': False},
        'core i5': {'LGA1700': True, 'LGA1200': True},
        'core i3': {'LGA1700': True, 'LGA1200': True},
        
        # AMD
        'ryzen 7': {'AM5': True, 'AM4': False},
        'ryzen 5': {'AM5': True, 'AM4': False},
        'ryzen 3': {'AM5': True, 'AM4': True},
        '5700X': {'AM4': True},
        '5950X': {'AM4': True},
    }
    
    # RAM type requirements by socket/chipset
    RAM_REQUIREMENTS = {
        'LGA1700': 'DDR5',
        'LGA1200': 'DDR4',
        'AM5': 'DDR5',
        'AM4': 'DDR4',
    }
    
    # GPU power requirements (in watts)
    GPU_TDP = {
        'RTX 4090': 450,
        'RTX 4080': 320,
        'RTX 4070': 200,
        'RTX 4070 SUPER': 220,
        'RTX 4060': 140,
        'RX 7900 XTX': 420,
        'RX 7900 XT': 360,
        'RX 7800 XT': 310,
        'RX 7700 XT': 250,
        'RX 6700': 200,
    }
    
    # CPU TDP (in watts)
    CPU_TDP = {
        'i7-13700K': 250,
        'i7-13700KF': 250,
        'i5-13600K': 181,
        'i5-13600KF': 181,
        'i3-13100': 60,
        'Ryzen 7 7700X': 105,
        'Ryzen 7 7700': 65,
        'Ryzen 5 7600X': 105,
        'Ryzen 5 7600': 65,
        'Ryzen 3 7100': 35,
    }
    
    # PSU wattage rating
    PSU_WATTAGE = {
        '450W': 450,
        '550W': 550,
        '650W': 650,
        '750W': 750,
        '850W': 850,
        '1000W': 1000,
        '1200W': 1200,
    }
    
    def analyze(self, components):
        """Analyze compatibility of selected components"""
        issues = []
        warnings = []
        
        cpu = components.get('cpu', '').lower()
        motherboard = components.get('motherboard', '').lower()
        ram = components.get('ram', '').lower()
        gpu = components.get('gpu', '').lower()
        psu = components.get('psu', '').lower()
        
        # Check CPU-Motherboard socket compatibility
        socket_issue = self._check_socket_compatibility(cpu, motherboard)
        if socket_issue:
            issues.append(socket_issue)
        
        # Check RAM compatibility
        ram_issue = self._check_ram_compatibility(motherboard, ram)
        if ram_issue:
            issues.append(ram_issue)
        
        # Check PSU wattage
        psu_warning = self._check_psu_wattage(cpu, gpu, psu)
        if psu_warning:
            warnings.append(psu_warning)
        
        # Check GPU PCIe compatibility (basic check)
        gpu_warning = self._check_gpu_compatibility(gpu, motherboard)
        if gpu_warning:
            warnings.append(gpu_warning)
        
        score = max(0, 100 - (len(issues) * 25) - (len(warnings) * 10))
        
        return {
            'issues': issues,
            'warnings': warnings,
            'details': self._generate_details(components, issues, warnings),
            'overall_score': score
        }
    
    def _check_socket_compatibility(self, cpu, motherboard):
        """Check if CPU socket matches motherboard socket"""
        if not cpu or not motherboard:
            return None
        
        # Detect motherboard socket more accurately
        mb_socket = None
        mb_lower = motherboard.lower()
        
        if 'lga1700' in mb_lower or 'z790' in mb_lower or 'b760' in mb_lower or 'h770' in mb_lower:
            mb_socket = 'LGA1700'
        elif 'lga1200' in mb_lower or 'z590' in mb_lower or 'b560' in mb_lower or 'h570' in mb_lower:
            mb_socket = 'LGA1200'
        elif 'am5' in mb_lower or 'x870' in mb_lower or 'x870e' in mb_lower or 'b850' in mb_lower:
            mb_socket = 'AM5'
        elif 'am4' in mb_lower or 'x570' in mb_lower or 'b550' in mb_lower or 'b450' in mb_lower:
            mb_socket = 'AM4'
        
        if not mb_socket:
            return None
        
        # Detect CPU socket requirements
        cpu_lower = cpu.lower()
        
        # Check for 13th/14th gen Intel (LGA1700 required)
        if any(x in cpu_lower for x in ['13700', '13600', '13100', '14700', '14600', '14100', 'i7-13', 'i5-13', 'i3-13', 'i7-14', 'i5-14', 'i3-14']):
            # These are LGA1700 CPUs
            if mb_socket not in ['LGA1700']:
                return f"CPU {cpu.split()[0]} requires LGA1700 socket, but motherboard has {mb_socket}"
        elif any(x in cpu_lower for x in ['12700', '12600', '12100', 'i7-12', 'i5-12', 'i3-12']):
            # 12th gen Intel - LGA1200
            if mb_socket not in ['LGA1200']:
                return f"CPU {cpu.split()[0]} requires LGA1200 socket, but motherboard has {mb_socket}"
        elif any(x in cpu_lower for x in ['7700', '7600', '7100', 'ryzen 7 7', 'ryzen 5 7']):
            # Ryzen 7000 series - AM5
            if mb_socket not in ['AM5']:
                return f"Ryzen 7000 series requires AM5 socket, but motherboard has {mb_socket}"
        elif any(x in cpu_lower for x in ['5950', '5900', '5800', '5700', '5600', '5500', 'ryzen 5950', 'ryzen 5900', 'ryzen 5800', 'ryzen 5700', 'ryzen 5600']):
            # Ryzen 5000 series - AM4
            if mb_socket not in ['AM4']:
                return f"Ryzen 5000 series requires AM4 socket, but motherboard has {mb_socket}"
        
        return None
    
    def _check_ram_compatibility(self, motherboard, ram):
        """Check if RAM type matches motherboard"""
        if not motherboard or not ram:
            return None
        
        # Detect motherboard socket/chipset
        mb_socket = None
        mb_lower = motherboard.lower()
        
        if 'lga1700' in mb_lower or 'z790' in mb_lower or 'b760' in mb_lower or 'h770' in mb_lower:
            mb_socket = 'LGA1700'
        elif 'lga1200' in mb_lower or 'z590' in mb_lower or 'b560' in mb_lower or 'h570' in mb_lower:
            mb_socket = 'LGA1200'
        elif 'am5' in mb_lower or 'x870' in mb_lower or 'x870e' in mb_lower or 'b850' in mb_lower:
            mb_socket = 'AM5'
        elif 'am4' in mb_lower or 'x570' in mb_lower or 'b550' in mb_lower or 'b450' in mb_lower:
            mb_socket = 'AM4'
        
        if not mb_socket:
            return None
        
        required_ram = self.RAM_REQUIREMENTS.get(mb_socket)
        if not required_ram:
            return None
        
        ram_upper = ram.upper()
        if required_ram not in ram_upper:
            return f"RAM type mismatch: {mb_socket} motherboard requires {required_ram}, but {ram} is selected"
        
        return None
    
    def _check_psu_wattage(self, cpu, gpu, psu):
        """Check if PSU wattage is sufficient for components"""
        if not cpu or not gpu or not psu:
            return None
        
        cpu_tdp = 65  # Default
        gpu_tdp = 200  # Default
        
        # Estimate CPU TDP
        for cpu_model, tdp in self.CPU_TDP.items():
            if cpu_model.lower() in cpu.lower():
                cpu_tdp = tdp
                break
        
        # Estimate GPU TDP
        for gpu_model, tdp in self.GPU_TDP.items():
            if gpu_model.lower() in gpu.lower():
                gpu_tdp = tdp
                break
        
        # Get PSU wattage
        psu_wattage = 550  # Default
        for wattage_str, watts in self.PSU_WATTAGE.items():
            if wattage_str in psu:
                psu_wattage = watts
                break
        
        # Calculate total power draw (with 30% overhead for efficiency)
        total_power = (cpu_tdp + gpu_tdp) * 1.3
        
        if total_power > psu_wattage:
            return f"PSU may be insufficient: {psu_wattage}W for ~{int(total_power)}W total load (too close to max capacity)"
        elif total_power > psu_wattage * 0.7:
            return f"PSU running near capacity: {psu_wattage}W for ~{int(total_power)}W load (consider higher wattage for longevity)"
        
        return None
    
    def _check_gpu_compatibility(self, gpu, motherboard):
        """Check basic GPU compatibility"""
        if not gpu or not motherboard:
            return None
        
        # Most modern GPUs work with modern boards, but check for very old combinations
        if 'rtx 40' in gpu.lower() or 'rx 7' in gpu.lower():
            # These need modern boards
            if 'x570' in motherboard.lower() or 'b650' in motherboard.lower() or 'z790' in motherboard.lower():
                return None
        
        return None
    
    def _generate_details(self, components, issues, warnings):
        """Generate a human-readable compatibility summary"""
        if not components or not any(components.values()):
            return "No components selected yet"
        
        count = sum(1 for v in components.values() if v)
        
        if issues:
            return f"{count} components - {len(issues)} critical issue(s) detected"
        elif warnings:
            return f"{count} components - {len(warnings)} warning(s) detected"
        else:
            return f"{count} components selected - Good compatibility!"
