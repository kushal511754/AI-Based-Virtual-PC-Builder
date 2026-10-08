"""Populate database with sample PC components."""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from server.utils.db import get_db_connection, init_db

def populate_database():
    """Insert sample PC components into database."""
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # CPUs
    cpus = [
        ('Intel Core i5-13600K', 'LGA1700', 14, 20, 3.5, 5.1, 125, 299, 'Intel'),
        ('Intel Core i7-13700K', 'LGA1700', 16, 24, 3.4, 5.4, 125, 449, 'Intel'),
        ('Intel Core i9-13900K', 'LGA1700', 24, 32, 3.0, 5.8, 125, 699, 'Intel'),
        ('AMD Ryzen 5 7600X', 'AM5', 6, 12, 4.7, 5.3, 105, 229, 'AMD'),
        ('AMD Ryzen 7 7700X', 'AM5', 8, 16, 4.5, 5.4, 105, 349, 'AMD'),
        ('AMD Ryzen 9 7950X', 'AM5', 16, 32, 4.5, 5.7, 162, 549, 'AMD'),
        ('Intel Core i3-13100', 'LGA1700', 4, 8, 3.4, 4.7, 65, 139, 'Intel'),
        ('AMD Ryzen 5 5600X', 'AM4', 6, 12, 3.7, 4.6, 65, 199, 'AMD'),
    ]
    
    for cpu in cpus:
        cursor.execute('''
            INSERT INTO cpu (name, socket_type, cores, threads, base_clock, turbo_clock, tdp, price, manufacturer)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', cpu)
    
    # GPUs
    gpus = [
        ('NVIDIA RTX 4090', 24, 'GDDR6X', 450, 320, 1599, 'NVIDIA', 2520),
        ('NVIDIA RTX 4080', 16, 'GDDR6X', 320, 290, 1199, 'NVIDIA', 2505),
        ('NVIDIA RTX 4070 Ti', 12, 'GDDR6X', 285, 285, 799, 'NVIDIA', 2310),
        ('NVIDIA RTX 4070', 12, 'GDDR6', 200, 245, 599, 'NVIDIA', 2310),
        ('NVIDIA RTX 4060 Ti', 8, 'GDDR6', 130, 165, 499, 'NVIDIA', 2670),
        ('AMD Radeon RX 7900 XTX', 24, 'GDDR6', 420, 420, 899, 'AMD', 2400),
        ('AMD Radeon RX 7900 XT', 20, 'GDDR6', 380, 420, 799, 'AMD', 2400),
        ('AMD Radeon RX 7800 XT', 16, 'GDDR6', 305, 320, 649, 'AMD', 2310),
    ]
    
    for gpu in gpus:
        cursor.execute('''
            INSERT INTO gpu (name, vram_gb, vram_type, power_draw, length_mm, price, manufacturer, memory_speed_mhz)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', gpu)
    
    # Motherboards
    motherboards = [
        ('ASUS ROG STRIX Z790-E', 'Z790', 'LGA1700', 'DDR5', 192, 'ATX', 479, 'ASUS'),
        ('MSI MAG B760 TOMAHAWK', 'B760', 'LGA1700', 'DDR5', 192, 'ATX', 199, 'MSI'),
        ('ASUS TUF Gaming X870-E', 'X870', 'AM5', 'DDR5', 192, 'ATX', 349, 'ASUS'),
        ('MSI MPG B850 EDGE', 'B850', 'AM5', 'DDR5', 192, 'ATX', 249, 'MSI'),
        ('ASRock B450 Pro RS', 'B450', 'AM4', 'DDR4', 64, 'ATX', 99, 'ASRock'),
        ('ASUS ProArt Z790', 'Z790', 'LGA1700', 'DDR5', 192, 'ATX', 699, 'ASUS'),
    ]
    
    for mobo in motherboards:
        cursor.execute('''
            INSERT INTO motherboard (name, chipset, socket_type, ram_type, max_ram_gb, form_factor, price, manufacturer)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', mobo)
    
    # RAM
    ram_modules = [
        ('Corsair Vengeance DDR5', 32, 'DDR5', 6000, 169.99, 'Corsair', 2),
        ('G.Skill Trident Z5', 32, 'DDR5', 6000, 189.99, 'G.Skill', 2),
        ('Kingston Fury Beast DDR5', 32, 'DDR5', 5600, 129.99, 'Kingston', 2),
        ('Corsair Vengeance DDR4', 16, 'DDR4', 3600, 79.99, 'Corsair', 2),
        ('G.Skill Ripjaws V', 16, 'DDR4', 3600, 69.99, 'G.Skill', 2),
        ('Crucial Ballistix', 16, 'DDR4', 3200, 59.99, 'Crucial', 2),
    ]
    
    for ram in ram_modules:
        cursor.execute('''
            INSERT INTO ram (name, size_gb, type, speed_mhz, price, manufacturer, modules)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', ram)
    
    # Storage
    storage = [
        ('Samsung 990 Pro 2TB', 'NVMe SSD', 2000, 7100, 229.99, 'Samsung'),
        ('WD Black SN850X 2TB', 'NVMe SSD', 2000, 7100, 199.99, 'Western Digital'),
        ('Crucial P5 Plus 2TB', 'NVMe SSD', 2000, 6600, 159.99, 'Crucial'),
        ('Samsung 870 QVO 2TB', 'SATA SSD', 2000, 550, 149.99, 'Samsung'),
        ('Seagate Barracuda 4TB', 'HDD', 4000, 7200, 79.99, 'Seagate'),
        ('WD Blue 4TB', 'HDD', 4000, 5400, 69.99, 'Western Digital'),
    ]
    
    for st in storage:
        cursor.execute('''
            INSERT INTO storage (name, type, capacity_gb, speed_rpm_or_mbps, price, manufacturer)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', st)
    
    # PSUs
    psus = [
        ('Corsair RM1000x', 1000, '80+ Gold', 179.99, 'Corsair', True),
        ('EVGA SuperNOVA 850 G5', 850, '80+ Gold', 139.99, 'EVGA', True),
        ('Seasonic Focus GX-750', 750, '80+ Gold', 119.99, 'Seasonic', True),
        ('MSI MAG A750GL', 750, '80+ Gold', 99.99, 'MSI', False),
        ('be quiet! Pure Power 12M', 650, '80+ Gold', 89.99, 'be quiet!', True),
        ('Corsair CV650', 650, '80+ Bronze', 69.99, 'Corsair', False),
    ]
    
    for psu in psus:
        cursor.execute('''
            INSERT INTO psu (name, wattage, efficiency_rating, price, manufacturer, modular)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', psu)
    
    # Cases
    cases = [
        ('NZXT H7 Flow', 420, 'Mid Tower', 149.99, 'NZXT', 1000),
        ('Corsair 5000T RGB', 430, 'Mid Tower', 299.99, 'Corsair', 1000),
        ('Lian Li LANCOOL 215', 320, 'Mid Tower', 49.99, 'Lian Li', 900),
        ('Fractal Design Meshify 2', 410, 'Mid Tower', 189.99, 'Fractal Design', 1000),
        ('Phanteks Eclipse P400A', 400, 'Mid Tower', 89.99, 'Phanteks', 900),
        ('Be Quiet! Pure Base 500DX', 400, 'Mid Tower', 99.99, 'be quiet!', 900),
    ]
    
    for case in cases:
        cursor.execute('''
            INSERT INTO pc_case (name, max_gpu_length_mm, form_factor, price, manufacturer, max_psu_wattage)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', case)
    
    # Cooling Solutions
    cooling = [
        ('Noctua NH-D15', 'Air', 'LGA1700', 220, 99.99, 'Noctua'),
        ('be quiet! Dark Rock Pro 4', 'Air', 'LGA1700', 250, 89.99, 'be quiet!'),
        ('Corsair H150i Elite', 'Liquid', 'LGA1700', 380, 199.99, 'Corsair'),
        ('NZXT Kraken X63', 'Liquid', 'LGA1700', 380, 179.99, 'NZXT'),
        ('Scythe Mugen 5 Rev.B', 'Air', 'AM5', 275, 54.99, 'Scythe'),
        ('Arctic Liquid Freezer II', 'Liquid', 'AM5', 420, 149.99, 'Arctic'),
    ]
    
    for cool in cooling:
        cursor.execute('''
            INSERT INTO cooling (name, type, socket_type, tdp_rating, price, manufacturer)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', cool)
    
    conn.commit()
    conn.close()
    print("✓ Database populated with sample components!")

if __name__ == '__main__':
    populate_database()
