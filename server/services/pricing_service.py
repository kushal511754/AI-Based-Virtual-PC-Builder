"""Pricing analysis service."""
from server.utils.db import get_db_connection, dict_from_row

class PricingService:
    def __init__(self):
        pass
    
    def analyze_build(self, cpu_id, motherboard_id, gpu_id, psu_id, case_id, ram_id, storage_id, cooling_id):
        """Analyze raw reference-catalogue prices, which are stored in USD."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        components = {}
        total_price = 0
        
        # Fetch all components
        if cpu_id:
            cursor.execute("SELECT * FROM cpu WHERE id = ?", (cpu_id,))
            cpu = dict_from_row(cursor.fetchone())
            if cpu:
                components['cpu'] = cpu
                total_price += cpu['price']
        
        if motherboard_id:
            cursor.execute("SELECT * FROM motherboard WHERE id = ?", (motherboard_id,))
            motherboard = dict_from_row(cursor.fetchone())
            if motherboard:
                components['motherboard'] = motherboard
                total_price += motherboard['price']
        
        if gpu_id:
            cursor.execute("SELECT * FROM gpu WHERE id = ?", (gpu_id,))
            gpu = dict_from_row(cursor.fetchone())
            if gpu:
                components['gpu'] = gpu
                total_price += gpu['price']
        
        if ram_id:
            cursor.execute("SELECT * FROM ram WHERE id = ?", (ram_id,))
            ram = dict_from_row(cursor.fetchone())
            if ram:
                components['ram'] = ram
                total_price += ram['price']
        
        if storage_id:
            cursor.execute("SELECT * FROM storage WHERE id = ?", (storage_id,))
            storage = dict_from_row(cursor.fetchone())
            if storage:
                components['storage'] = storage
                total_price += storage['price']
        
        if psu_id:
            cursor.execute("SELECT * FROM psu WHERE id = ?", (psu_id,))
            psu = dict_from_row(cursor.fetchone())
            if psu:
                components['psu'] = psu
                total_price += psu['price']
        
        if case_id:
            cursor.execute("SELECT * FROM pc_case WHERE id = ?", (case_id,))
            case = dict_from_row(cursor.fetchone())
            if case:
                components['case'] = case
                total_price += case['price']
        
        if cooling_id:
            cursor.execute("SELECT * FROM cooling WHERE id = ?", (cooling_id,))
            cooling = dict_from_row(cursor.fetchone())
            if cooling:
                components['cooling'] = cooling
                total_price += cooling['price']
        
        conn.close()
        
        # Calculate breakdowns
        price_breakdown = self._calculate_breakdown(components)
        suggestions = self._generate_suggestions(components, cpu_id, gpu_id)
        
        return {
            'total_price': round(total_price, 2),
            'breakdown': price_breakdown,
            'suggestions': suggestions,
            'components': components,
            'currency': 'USD',
            'display_currency': 'INR',
            'conversion_rate': 83,
            'price_source': 'Local reference catalogue (USD converted for INR display)'
        }
    
    def _calculate_breakdown(self, components):
        """Calculate cost breakdown by category."""
        breakdown = {}
        for category, component in components.items():
            if component:
                breakdown[category] = round(component['price'], 2)
        return breakdown
    
    def _generate_suggestions(self, components, cpu_id, gpu_id):
        """Generate upgrade/downgrade suggestions."""
        suggestions = []
        
        if cpu_id and 'cpu' in components:
            cpu = components['cpu']
            if cpu['cores'] >= 16 and cpu['price'] > 500:
                suggestions.append("Consider a mid-range CPU for general use (save ₹16,600-24,900)")
        
        if gpu_id and 'gpu' in components:
            gpu = components['gpu']
            if gpu['vram_gb'] >= 24 and gpu['price'] > 1500:
                suggestions.append("High-end GPU selected - ensure PSU is adequate for power draw")
        
        if 'cpu' in components and 'gpu' in components:
            cpu = components['cpu']
            gpu = components['gpu']
            
            # Check for bottleneck
            if cpu['cores'] <= 4 and gpu['vram_gb'] >= 8:
                suggestions.append("⚠️ Potential CPU bottleneck - Consider upgrading CPU")
            elif cpu['cores'] >= 16 and gpu['vram_gb'] <= 4:
                suggestions.append("⚠️ Potential GPU bottleneck - Consider upgrading GPU")
        
        # RAM suggestions
        if 'ram' in components:
            ram = components['ram']
            if ram['size_gb'] < 16:
                suggestions.append("Consider 16GB+ RAM for better multitasking (upgrade to ₹8,300-12,450)")
        
        return suggestions
