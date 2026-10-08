"""Database models - Motherboard."""

class Motherboard:
    def __init__(self, id, name, chipset, socket_type, ram_type, max_ram_gb, form_factor, price, manufacturer):
        self.id = id
        self.name = name
        self.chipset = chipset
        self.socket_type = socket_type
        self.ram_type = ram_type
        self.max_ram_gb = max_ram_gb
        self.form_factor = form_factor
        self.price = price
        self.manufacturer = manufacturer
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'chipset': self.chipset,
            'socket_type': self.socket_type,
            'ram_type': self.ram_type,
            'max_ram_gb': self.max_ram_gb,
            'form_factor': self.form_factor,
            'price': self.price,
            'manufacturer': self.manufacturer
        }
