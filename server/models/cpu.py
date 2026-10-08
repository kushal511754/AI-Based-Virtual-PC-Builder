"""Database models - CPU."""

class CPU:
    def __init__(self, id, name, socket_type, cores, threads, base_clock, turbo_clock, tdp, price, manufacturer):
        self.id = id
        self.name = name
        self.socket_type = socket_type
        self.cores = cores
        self.threads = threads
        self.base_clock = base_clock
        self.turbo_clock = turbo_clock
        self.tdp = tdp
        self.price = price
        self.manufacturer = manufacturer
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'socket_type': self.socket_type,
            'cores': self.cores,
            'threads': self.threads,
            'base_clock': self.base_clock,
            'turbo_clock': self.turbo_clock,
            'tdp': self.tdp,
            'price': self.price,
            'manufacturer': self.manufacturer
        }
