"""Database models - GPU."""

class GPU:
    def __init__(self, id, name, vram_gb, vram_type, power_draw, length_mm, price, manufacturer, memory_speed_mhz):
        self.id = id
        self.name = name
        self.vram_gb = vram_gb
        self.vram_type = vram_type
        self.power_draw = power_draw
        self.length_mm = length_mm
        self.price = price
        self.manufacturer = manufacturer
        self.memory_speed_mhz = memory_speed_mhz
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'vram_gb': self.vram_gb,
            'vram_type': self.vram_type,
            'power_draw': self.power_draw,
            'length_mm': self.length_mm,
            'price': self.price,
            'manufacturer': self.manufacturer,
            'memory_speed_mhz': self.memory_speed_mhz
        }
