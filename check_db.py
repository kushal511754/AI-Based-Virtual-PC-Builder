from server.utils.db import get_db

with get_db() as conn:
    cursor = conn.cursor()
    
    # Check CPU
    cursor.execute('SELECT COUNT(*) FROM cpu')
    print(f'CPUs: {cursor.fetchone()[0]}')
    
    # Check GPU
    cursor.execute('SELECT COUNT(*) FROM gpu')
    print(f'GPUs: {cursor.fetchone()[0]}')
    
    # Check RAM
    cursor.execute('SELECT COUNT(*) FROM ram')
    print(f'RAM: {cursor.fetchone()[0]}')
    
    # Check Motherboard
    cursor.execute('SELECT COUNT(*) FROM motherboard')
    print(f'Motherboards: {cursor.fetchone()[0]}')
    
    # Check Storage
    cursor.execute('SELECT COUNT(*) FROM storage')
    print(f'Storage: {cursor.fetchone()[0]}')
    
    # Check PSU
    cursor.execute('SELECT COUNT(*) FROM psu')
    print(f'PSU: {cursor.fetchone()[0]}')
    
    # Check Case
    cursor.execute('SELECT COUNT(*) FROM pc_case')
    print(f'Cases: {cursor.fetchone()[0]}')
    
    # Check Cooling
    cursor.execute('SELECT COUNT(*) FROM cooling')
    print(f'Cooling: {cursor.fetchone()[0]}')
