import sqlite3
import os
from contextlib import contextmanager

DATABASE_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'database.db')

def get_db_connection():
    """Get a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@contextmanager
def get_db():
    """Context manager for database connections."""
    conn = get_db_connection()
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def init_db():
    """Initialize the database with tables."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # CPU Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cpu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            socket_type TEXT NOT NULL,
            cores INTEGER NOT NULL,
            threads INTEGER NOT NULL,
            base_clock REAL NOT NULL,
            turbo_clock REAL NOT NULL,
            tdp INTEGER NOT NULL,
            price REAL NOT NULL,
            manufacturer TEXT NOT NULL
        )
    ''')
    
    # GPU Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gpu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            vram_gb INTEGER NOT NULL,
            vram_type TEXT NOT NULL,
            power_draw INTEGER NOT NULL,
            length_mm INTEGER NOT NULL,
            price REAL NOT NULL,
            manufacturer TEXT NOT NULL,
            memory_speed_mhz INTEGER NOT NULL
        )
    ''')
    
    # Motherboard Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS motherboard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            chipset TEXT NOT NULL,
            socket_type TEXT NOT NULL,
            ram_type TEXT NOT NULL,
            max_ram_gb INTEGER NOT NULL,
            form_factor TEXT NOT NULL,
            price REAL NOT NULL,
            manufacturer TEXT NOT NULL
        )
    ''')
    
    # RAM Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ram (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            size_gb INTEGER NOT NULL,
            type TEXT NOT NULL,
            speed_mhz INTEGER NOT NULL,
            price REAL NOT NULL,
            manufacturer TEXT NOT NULL,
            modules INTEGER NOT NULL
        )
    ''')
    
    # Storage Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS storage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            capacity_gb INTEGER NOT NULL,
            speed_rpm_or_mbps INTEGER,
            price REAL NOT NULL,
            manufacturer TEXT NOT NULL
        )
    ''')
    
    # PSU Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS psu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            wattage INTEGER NOT NULL,
            efficiency_rating TEXT NOT NULL,
            price REAL NOT NULL,
            manufacturer TEXT NOT NULL,
            modular BOOLEAN NOT NULL
        )
    ''')
    
    # Case Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pc_case (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            max_gpu_length_mm INTEGER NOT NULL,
            form_factor TEXT NOT NULL,
            price REAL NOT NULL,
            manufacturer TEXT NOT NULL,
            max_psu_wattage INTEGER NOT NULL
        )
    ''')
    
    # Cooling Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cooling (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            socket_type TEXT NOT NULL,
            tdp_rating INTEGER NOT NULL,
            price REAL NOT NULL,
            manufacturer TEXT NOT NULL
        )
    ''')
    
    # Saved Builds Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS saved_build (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            build_name TEXT NOT NULL,
            cpu_id INTEGER,
            gpu_id INTEGER,
            motherboard_id INTEGER,
            ram_id INTEGER,
            storage_id INTEGER,
            psu_id INTEGER,
            case_id INTEGER,
            cooling_id INTEGER,
            total_price REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (cpu_id) REFERENCES cpu(id),
            FOREIGN KEY (gpu_id) REFERENCES gpu(id),
            FOREIGN KEY (motherboard_id) REFERENCES motherboard(id),
            FOREIGN KEY (ram_id) REFERENCES ram(id),
            FOREIGN KEY (storage_id) REFERENCES storage(id),
            FOREIGN KEY (psu_id) REFERENCES psu(id),
            FOREIGN KEY (case_id) REFERENCES pc_case(id),
            FOREIGN KEY (cooling_id) REFERENCES cooling(id)
        )
    ''')
    
    # Domain Requirements Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS domain_requirements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            domain_name TEXT NOT NULL UNIQUE,
            min_cpu_cores INTEGER NOT NULL,
            min_gpu_vram INTEGER NOT NULL,
            min_ram_gb INTEGER NOT NULL,
            min_storage_gb INTEGER NOT NULL,
            recommended_psu_wattage INTEGER NOT NULL,
            description TEXT
        )
    ''')
    
    # Game Requirements Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS game_requirements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_name TEXT NOT NULL,
            min_cpu_cores INTEGER,
            min_gpu_vram INTEGER,
            min_ram_gb INTEGER,
            recommended_cpu_cores INTEGER,
            recommended_gpu_vram INTEGER,
            recommended_ram_gb INTEGER,
            estimated_budget_low REAL,
            estimated_budget_high REAL,
            release_year INTEGER
        )
    ''')
    
    # AI Build History Table (for tracking AI suggestions)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ai_build_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            domain TEXT NOT NULL,
            game_or_task TEXT,
            budget REAL NOT NULL,
            suggested_cpu_id INTEGER,
            suggested_gpu_id INTEGER,
            suggested_motherboard_id INTEGER,
            suggested_ram_id INTEGER,
            suggested_storage_id INTEGER,
            suggested_psu_id INTEGER,
            suggested_case_id INTEGER,
            suggested_cooling_id INTEGER,
            total_suggested_price REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Users Table for authentication
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def dict_from_row(row):
    """Convert sqlite3.Row to dict."""
    if row is None:
        return None
    return dict(row)
