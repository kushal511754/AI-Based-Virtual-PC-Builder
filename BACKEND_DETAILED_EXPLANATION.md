# 🔧 Backend Architecture - Detailed Explanation

## Overview
The backend is a **Flask-based REST API** that powers the PC Builder application. It handles:
- User authentication
- Component database management
- Build validation & compatibility checking
- AI-powered recommendations
- ML-based predictions
- Data persistence

---

## 1. APPLICATION INITIALIZATION (app.py)

### Purpose
`app.py` is the **main entry point** that bootstraps the entire Flask application.

### Key Functions

```python
def create_app():
    """Creates and configures the Flask application."""
    
    # Step 1: Create Flask instance with folder configurations
    app = Flask(__name__, 
                template_folder='../templates',    # HTML files location
                static_folder='../static')         # CSS/JS files location
    
    # Step 2: Configure Flask settings
    app.config['PROPAGATE_EXCEPTIONS'] = True      # Better error handling
    app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True
    app.config['JSON_SORT_KEYS'] = False           # Preserve JSON order
    
    # Step 3: Initialize database (create tables if needed)
    _init_db_once()
    
    # Step 4: Register all API route blueprints
    blueprints = [
        'auth',           # /api/auth/* - Login/signup
        'parts',          # /api/parts/* - Component queries
        'builder',        # /api/builder/* - Build operations
        'games',          # /api/games/* - Game data
        'compatibility',  # /api/compatibility/* - Validation
        'ai_build',       # /api/ai/* - AI suggestions
        'ml_routes',      # /api/ml/* - ML predictions
        'search',         # /api/search/* - Search functionality
    ]
    
    # Step 5: Register error handlers
    @app.errorhandler(404)
    @app.errorhandler(500)
    
    return app
```

### Flow Diagram
```
run.py
  ↓
app.run() → create_app()
  ↓
1. Create Flask instance
  ↓
2. Set configurations
  ↓
3. Initialize SQLite database
  ↓
4. Load all blueprints (route modules)
  ↓
5. Setup error handlers
  ↓
6. Start server on port 5000
  ↓
Ready to handle requests
```

---

## 2. ROUTING LAYER

The routing layer consists of **10 Flask blueprints** that define API endpoints. Each blueprint handles a specific feature area.

### 2.1 Authentication Routes (`routes/auth.py`)

**Purpose:** Handle user login, registration, and password validation

**Endpoints:**

```
POST /api/auth/login
├─ Input: { email, password }
├─ Process:
│  ├─ Validate email format
│  ├─ Check if email exists in users table
│  ├─ Compare hashed passwords
│  └─ Return user data or error
└─ Output: { success, user, token }

POST /api/auth/register
├─ Input: { email, username, password }
├─ Process:
│  ├─ Validate all fields
│  ├─ Check if email/username already exists
│  ├─ Hash password with SHA256
│  ├─ Insert into users table
│  └─ Return user_id
└─ Output: { success, user_id }

POST /api/auth/check-email
├─ Input: { email }
├─ Output: { available: boolean }

POST /api/auth/check-username
├─ Input: { username }
└─ Output: { available: boolean }
```

**Code Example:**
```python
@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user."""
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    # Validate inputs
    if not email or not password:
        return jsonify({'error': 'Missing fields'}), 400
    
    # Query database
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
    
    # Check password
    if user and hash_password(password) == user['password']:
        return jsonify({'success': True, 'user': {...}})
    
    return jsonify({'error': 'Invalid credentials'}), 401
```

### 2.2 Parts Routes (`routes/parts.py`)

**Purpose:** Retrieve PC components from database

**Endpoints:**

```
GET /api/parts/cpu
├─ Returns: [{ id, name, cores, price, manufacturer, ... }, ...]

GET /api/parts/gpu
├─ Returns: GPU components with specs

GET /api/parts/motherboard
├─ Returns: Motherboards with socket types

GET /api/parts/ram
├─ Returns: RAM modules with speeds

GET /api/parts/storage
├─ Returns: SSDs and HDDs

GET /api/parts/psu
├─ Returns: Power supplies with ratings

GET /api/parts/case
├─ Returns: Cases with dimensions

GET /api/parts/cooling
└─ Returns: CPU coolers with TDP ratings
```

**Key Logic:**
```python
class PartService:
    @staticmethod
    def get_all_cpus():
        """Fetch all CPUs from database."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Query with sorting
        cursor.execute(
            "SELECT * FROM cpu ORDER BY price ASC"
        )
        
        # Convert rows to dictionaries
        cpus = [dict_from_row(row) for row in cursor.fetchall()]
        conn.close()
        
        return cpus
```

### 2.3 Builder Routes (`routes/builder.py`)

**Purpose:** Handle build operations (save, load, validate)

**Endpoints:**

```
GET /api/builder/parts
├─ Returns all components organized by type
├─ Used by UI to populate dropdown menus

POST /api/builder/validate
├─ Input: { cpu_id, gpu_id, motherboard_id, ram_id, 
│           storage_id, psu_id, case_id, cooling_id }
├─ Validates entire build compatibility
└─ Returns: { compatible, errors, warnings }

POST /api/builder/save
├─ Input: { build_name, components, total_price }
├─ Saves build to saved_build table
└─ Returns: { success, build_id }

GET /api/builder/builds
├─ Returns all user's saved builds

GET /api/builder/build/<id>
├─ Returns specific build details

DELETE /api/builder/build/<id>
└─ Deletes a saved build
```

### 2.4 Compatibility Routes (`routes/compatibility.py`)

**Purpose:** Detailed component compatibility checking

**Endpoints:**

```
POST /api/compatibility/check
├─ Input: { cpu_id, motherboard_id, gpu_id, psu_id, ... }
├─ Performs multiple validation checks
└─ Returns detailed compatibility report

GET /api/compatibility/socket/<socket_type>
├─ Returns compatible motherboards for CPU socket
├─ Used to filter motherboard dropdowns

GET /api/compatibility/ram/<motherboard_id>
└─ Returns compatible RAM for motherboard
```

### 2.5 AI Build Routes (`routes/ai_build.py`)

**Purpose:** AI-powered PC build recommendations

**Endpoints:**

```
GET /api/ai/domains
├─ Returns available domains (Gaming, Video Editing, etc.)

POST /api/ai/suggest-build
├─ Input: { domain, budget_usd, game_or_task }
├─ Process:
│  ├─ Get domain requirements
│  ├─ Filter components within budget
│  ├─ Check compatibility
│  ├─ Calculate pricing
│  └─ Return optimized build
└─ Returns: { success, build, price_breakdown, suggestions }

POST /api/ai/refine-build
├─ Input: { current_build, adjustment_type }
└─ Returns: refined build suggestion
```

### 2.6 Search Routes (`routes/search.py`)

**Purpose:** Component search and filtering

**Endpoints:**

```
GET /api/search?q=query&type=component_type
├─ Full-text search across components
├─ Filters by price, specs, manufacturer
└─ Returns ranked results

GET /api/search/cpu?cores=8&price_max=500
├─ Filtered search with parameters
└─ Returns matching components
```

### 2.7 Game Routes (`routes/games.py`)

**Purpose:** Game-specific requirements lookup

**Endpoints:**

```
GET /api/games
├─ Returns list of popular games

GET /api/games/<game_id>
├─ Returns game specifications & requirements

POST /api/games/search?q=game_name
└─ Search for game by name
```

### 2.8 ML Routes (`routes/ml_routes.py`)

**Purpose:** Machine learning predictions

**Endpoints:**

```
POST /api/ml/predict-performance
├─ Input: { components }
├─ Predicts FPS/performance
└─ Returns: { estimated_fps, confidence }

POST /api/ml/recommend-upgrade
├─ Input: { current_build, budget }
├─ Suggests best upgrades
└─ Returns: { upgrade_path, performance_gain }

GET /api/ml/models/status
└─ Returns status of trained ML models
```

---

## 3. SERVICE LAYER

The service layer contains **business logic** that processes data. Each service handles a specific domain.

### 3.1 Part Service (`services/part_service.py`)

**Responsibility:** Component database queries and filtering

**Key Methods:**
```python
class PartService:
    # Get all components
    get_all_parts()           # Returns dict of all components by type
    get_all_cpus()            # Query CPU table
    get_all_gpus()            # Query GPU table
    get_cpu_by_socket(socket) # Filter CPUs by socket type
    
    # Search and filter
    search_components(query)  # Full-text search
    filter_by_price(type, max_price)
    filter_by_specs(type, specs_dict)
    
    # Get specific component
    get_component_by_id(type, id)
```

**Example Usage:**
```python
# In route handler
service = PartService()

# Get all CPUs
cpus = service.get_all_cpus()
# Returns: [
#   {id: 1, name: "Intel i5-13400", cores: 10, price: 250},
#   {id: 2, name: "AMD Ryzen 5 5600X", cores: 6, price: 200},
#   ...
# ]

# Filter by socket
cpus_lga1700 = service.filter_by_socket('LGA1700')

# Filter by budget
cpus_budget = service.filter_by_price('cpu', max_price=300)
```

### 3.2 Compatibility Engine (`services/compatibility_engine.py`)

**Responsibility:** Validate component compatibility

**Validation Checks:**

```python
class CompatibilityEngine:
    def validate_build(self, cpu_id, motherboard_id, gpu_id, 
                       psu_id, case_id, ram_id, cooling_id):
        """Main validation method."""
        
        # Check 1: CPU ↔ Motherboard Socket
        _check_socket_compatibility(cpu, motherboard)
        # CPU socket must match motherboard socket
        # Example: LGA1700 CPU needs LGA1700 motherboard
        
        # Check 2: RAM ↔ Motherboard
        _check_ram_compatibility(ram, motherboard)
        # RAM type (DDR5 vs DDR4) must match motherboard
        # RAM size must not exceed motherboard max
        
        # Check 3: GPU ↔ PSU
        _check_power_compatibility(cpu, gpu, psu)
        # Total power draw (CPU + GPU) ≤ PSU capacity - 150W buffer
        # PSU must have enough headroom
        
        # Check 4: GPU ↔ Case
        _check_case_compatibility(gpu, case)
        # GPU length must fit in case max GPU length
        # Prevents physical fit issues
        
        # Check 5: Cooling ↔ CPU
        _check_cooling_compatibility(cooling, cpu)
        # Cooler TDP rating must cover CPU TDP
        # Prevents overheating
        
        return {
            'compatible': True/False,
            'errors': [list of critical issues],
            'warnings': [list of minor issues]
        }
```

**Return Format:**
```python
{
    'compatible': True,
    'errors': [
        'CPU socket LGA1700 not compatible with motherboard socket AM5'
    ],
    'warnings': [
        'CPU TDP 125W exceeds cooler capacity 120W',
        'PSU only has 100W headroom (recommended 150W)'
    ]
}
```

### 3.3 Pricing Service (`services/pricing_service.py`)

**Responsibility:** Price calculations and analysis

**Key Methods:**
```python
class PricingService:
    # Calculate totals
    calculate_build_total(components)      # Sum all prices
    calculate_price_per_component(build)   # Breakdown by type
    
    # Analysis
    calculate_cost_per_performance(build, game)
    detect_bottleneck(cpu, gpu, budget)    # Find mismatch
    
    # Suggestions
    get_upgrade_suggestions(current_build, budget)
    get_downgrade_suggestions(current_build, target_price)
    
    # Comparison
    compare_builds(build1, build2)         # Show differences
```

**Example:**
```python
service = PricingService()

build_data = {
    'cpu': {'price': 250},
    'gpu': {'price': 400},
    'motherboard': {'price': 150},
    'ram': {'price': 100},
    'storage': {'price': 80},
    'psu': {'price': 100},
    'case': {'price': 70},
    'cooling': {'price': 0}
}

# Calculate total
total = service.calculate_build_total(build_data)
# Returns: 1150

# Get breakdown
breakdown = service.calculate_price_per_component(build_data)
# Returns: {
#   'cpu': {'price': 250, 'percentage': 21.7%},
#   'gpu': {'price': 400, 'percentage': 34.8%},
#   ...
# }

# Detect bottleneck
bottleneck = service.detect_bottleneck(cpu_i5, gpu_rtx3090, budget_1200)
# Returns: {'bottleneck': 'GPU too powerful for CPU', 'advice': '...'}
```

### 3.4 AI Build Service (`services/ai_build_service.py`)

**Responsibility:** AI-powered build recommendations

**Key Methods:**
```python
class AIBuildService:
    # Domain management
    get_domains()                          # Return available domains
    get_domain_requirements(domain)        # Get specs for domain
    
    # Build generation
    get_ai_suggestion(domain, budget_usd, game_or_task)
    
    # Caching (1-hour cache for repeated requests)
    _cache_result(key, value)
    _get_cached_result(key)
```

**Domain Specifications:**
```python
DOMAINS = {
    'gaming': {
        'min_cpu_cores': 6,
        'min_gpu_vram': 4,
        'min_ram_gb': 16,
        'min_storage_gb': 500,
        'priority': 'gpu'  # GPU matters most
    },
    'video_editing': {
        'min_cpu_cores': 8,
        'min_gpu_vram': 6,
        'min_ram_gb': 32,
        'min_storage_gb': 2000,
        'priority': 'cpu'  # CPU matters most
    },
    'programming': {
        'min_cpu_cores': 4,
        'min_gpu_vram': 2,
        'min_ram_gb': 16,
        'min_storage_gb': 512,
        'priority': 'cpu'
    },
    'streaming': {
        'min_cpu_cores': 8,
        'min_gpu_vram': 4,
        'min_ram_gb': 24,
        'priority': 'balanced'
    },
    'rendering': {
        'min_cpu_cores': 16,
        'min_gpu_vram': 8,
        'min_ram_gb': 64,
        'priority': 'gpu'
    }
}
```

**AI Suggestion Flow:**
```python
def get_ai_suggestion(domain, budget, game):
    """Generate AI-powered build suggestion."""
    
    # Step 1: Get domain requirements
    domain_specs = self.get_domain_requirements(domain)
    
    # Step 2: Validate budget meets minimum
    if budget < domain_specs.get('min_budget'):
        return error('Budget too low')
    
    # Step 3: Select components based on budget
    cpu = select_cpu(domain, budget)           # Pick CPU
    gpu = select_gpu(domain, budget)           # Pick GPU
    motherboard = select_motherboard(cpu)      # Pick compatible motherboard
    ram = select_ram(domain, budget)           # Pick RAM
    storage = select_storage(domain, budget)   # Pick storage
    psu = select_psu(cpu, gpu, budget)        # Pick PSU
    case = select_case(budget)                 # Pick case
    cooling = select_cooling(cpu)              # Pick cooler
    
    # Step 4: Validate compatibility
    validation = CompatibilityEngine().validate_build(...)
    if not validation['compatible']:
        return adjust_selection()  # Try different components
    
    # Step 5: Calculate pricing
    total = sum([cpu.price, gpu.price, ...])
    
    # Step 6: Generate suggestions
    suggestions = [
        "GPU is the bottleneck for gaming",
        "Consider upgrading GPU to RTX 4070",
        "Storage is sufficient but SSD speed could improve boot times"
    ]
    
    return {
        'success': True,
        'cpu': cpu,
        'gpu': gpu,
        'motherboard': motherboard,
        'ram': ram,
        'storage': storage,
        'psu': psu,
        'case': case,
        'cooling': cooling,
        'total_price': total,
        'suggestions': suggestions,
        'validation': validation
    }
```

### 3.5 Build Service (`services/build_service.py`)

**Responsibility:** Save and manage user builds

**Key Methods:**
```python
class BuildService:
    # CRUD operations
    save_build(user_id, build_name, components)      # Create
    load_build(user_id, build_id)                    # Read
    get_user_builds(user_id)                         # Read all
    update_build(user_id, build_id, components)      # Update
    delete_build(user_id, build_id)                  # Delete
```

**Database Schema:**
```sql
CREATE TABLE saved_build (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    build_name TEXT,
    cpu_id INTEGER,
    gpu_id INTEGER,
    motherboard_id INTEGER,
    ram_id INTEGER,
    storage_id INTEGER,
    psu_id INTEGER,
    case_id INTEGER,
    cooling_id INTEGER,
    total_price REAL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

### 3.6 Game Database Service (`services/game_database_service.py`)

**Responsibility:** Game specifications lookup

**Key Methods:**
```python
class GameDatabaseService:
    get_all_games()                           # Get popular games list
    get_game_requirements(game_id)            # CPU/GPU specs
    get_game_by_name(game_name)              # Search by name
    classify_game_tier(game_name)            # Low/Medium/High/Ultra tier
    get_recommended_build(game_name)          # Build for this game
```

### 3.7 ML Services

**ML Build Recommender (`ml_build_recommender.py`):**
```python
class MLBuildRecommender:
    # Trained models for recommendations
    recommend_build(domain, budget)          # ML-based suggestion
    predict_performance(components)          # FPS/performance prediction
    suggest_upgrade(current_build, budget)   # Upgrade path recommendation
```

**ML Game Classifier (`ml_game_classifier.py`):**
```python
class MLGameClassifier:
    classify_game_tier(game_name)            # Low/Medium/High/Ultra
    get_required_specs(game_name)            # Predicted requirements
    estimate_performance(game, components)   # FPS estimate
```

---

## 4. DATABASE LAYER

### 4.1 Database Connection (`utils/db.py`)

**Purpose:** Manage SQLite database connections

```python
import sqlite3

# Database file location
DATABASE_PATH = 'database.db'

def get_db_connection():
    """Create a new database connection."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # Enable dict-like access
    return conn

@contextmanager
def get_db():
    """Context manager for safe connection handling."""
    conn = get_db_connection()
    try:
        yield conn
        conn.commit()  # Auto-commit on success
    except Exception as e:
        conn.rollback()  # Auto-rollback on error
        raise e
    finally:
        conn.close()  # Always close connection
```

**Usage Example:**
```python
from server.utils.db import get_db

# Safe database query with automatic commit/rollback
with get_db() as conn:
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    
    if user:
        # Update user
        cursor.execute('UPDATE users SET ... WHERE id = ?', (user_id,))
        # Commit happens automatically here
```

### 4.2 Database Initialization

```python
def init_db():
    """Create all tables on startup."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            email TEXT UNIQUE,
            username TEXT UNIQUE,
            password TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create component tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cpu (
            id INTEGER PRIMARY KEY,
            name TEXT,
            socket_type TEXT,
            cores INTEGER,
            threads INTEGER,
            base_clock REAL,
            turbo_clock REAL,
            tdp INTEGER,
            price REAL,
            manufacturer TEXT
        )
    ''')
    
    # ... similar for gpu, motherboard, ram, storage, psu, case, cooling
    
    # Create build tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS saved_build (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            build_name TEXT,
            cpu_id INTEGER,
            gpu_id INTEGER,
            ...
            total_price REAL,
            created_at TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
```

### 4.3 Tables Overview

```
┌─ Users ─────────────────────────────────┐
│ id | email | username | password | ...  │
└─────────────────────────────────────────┘

┌─ CPU ────────────────────────────────────┐
│ id | name | socket | cores | price | .. │
└──────────────────────────────────────────┘

┌─ GPU ────────────────────────────────────┐
│ id | name | vram | power | length | ... │
└──────────────────────────────────────────┘

┌─ Motherboard ────────────────────────────┐
│ id | name | socket | ram_type | price.. │
└──────────────────────────────────────────┘

┌─ RAM ────────────────────────────────────┐
│ id | name | size | type | speed | price │
└──────────────────────────────────────────┘

┌─ Storage ────────────────────────────────┐
│ id | name | type | capacity | price | .. │
└──────────────────────────────────────────┘

┌─ PSU ────────────────────────────────────┐
│ id | name | wattage | efficiency | price │
└──────────────────────────────────────────┘

┌─ Case ────────────────────────────────────┐
│ id | name | gpu_length | form_factor | p │
└───────────────────────────────────────────┘

┌─ Cooling ────────────────────────────────┐
│ id | name | type | socket | tdp | price │
└──────────────────────────────────────────┘

┌─ SavedBuild ─────────────────────────────┐
│ id | user_id | build_name | cpu_id | ... │
│    |         | total_price | date | ...  │
└──────────────────────────────────────────┘

┌─ DomainRequirements ─────────────────────┐
│ id | domain | min_cores | min_gpu | ...  │
└──────────────────────────────────────────┘

┌─ GameRequirements ───────────────────────┐
│ id | game_name | min_cpu | min_gpu | ... │
└──────────────────────────────────────────┘
```

---

## 5. REQUEST-RESPONSE CYCLE

### Example: Building a PC (Manual Mode)

```
USER INTERFACE                          BACKEND
─────────────────────────────────────────────────────────────

User selects components
(dropdown menus)
         ↓
"Check Compatibility" click
         ↓
JavaScript sends:
POST /api/builder/validate
{
    cpu_id: 5,
    gpu_id: 12,
    motherboard_id: 3,
    ram_id: 8,
    ...
}
                                    ↓ Request received
                            routes/builder.py::validate_build()
                                    ↓
                            CompatibilityEngine.validate_build()
                                    ↓
                            1. Check socket compatibility
                            2. Check RAM compatibility
                            3. Check power requirements
                            4. Check physical fit
                            5. Check cooling capacity
                                    ↓
                        Return validation result
                                    ↓
Response:
{
    compatible: true,
    errors: [],
    warnings: [
        "PSU has limited headroom"
    ]
}
         ↓
JavaScript displays:
✓ Build is compatible
⚠ PSU has limited headroom
         ↓
User clicks "Save Build"
         ↓
POST /api/builder/save
{
    build_name: "Gaming 1080p",
    cpu_id: 5,
    gpu_id: 12,
    ...
}
                                    ↓
                        routes/builder.py::save_build()
                                    ↓
                        BuildService.save_build()
                                    ↓
                        INSERT into saved_build table
                                    ↓
                        Commit to database
                                    ↓
Response:
{
    success: true,
    build_id: 42,
    message: "Build saved successfully"
}
         ↓
JavaScript displays:
"Build saved! View in My Builds"
```

### Example: AI Build Suggestion

```
USER INTERFACE                          BACKEND
─────────────────────────────────────────────────────────────

User selects domain: "Gaming"
User enters budget: $1000
User enters game: "Cyberpunk 2077"
         ↓
"Get Suggestion" click
         ↓
POST /api/ai/suggest-build
{
    domain: "gaming",
    budget_usd: 1000,
    game: "Cyberpunk 2077"
}
                                    ↓
                        routes/ai_build.py::suggest_build()
                                    ↓
                        AIBuildService.get_ai_suggestion()
                                    ↓
                        Step 1: Get domain requirements
                        {
                            min_cpu_cores: 6,
                            min_gpu_vram: 4,
                            min_ram_gb: 16,
                            priority: 'gpu'
                        }
                                    ↓
                        Step 2: Validate budget
                        if budget < minimum:
                            return error
                                    ↓
                        Step 3: Component selection
                        - Select CPU: Intel i5-13400 ($250)
                        - Select GPU: RTX 4060 Ti ($400)
                        - Select Motherboard: B760M ($120)
                        - Select RAM: 16GB DDR5 ($80)
                        - Select Storage: 1TB NVMe ($90)
                        - Select PSU: 750W ($100)
                        - Select Case: Mid-tower ($70)
                        - Select Cooler: Stock ($0)
                                    ↓
                        Step 4: Validate compatibility
                        CompatibilityEngine.validate_build(...)
                                    ↓
                        Step 5: Calculate totals
                        Total: $1110
                                    ↓
                        Step 6: Generate suggestions
                        [
                            "Excellent GPU for 1440p gaming",
                            "CPU handles gaming well",
                            "RAM is sufficient"
                        ]
                                    ↓
Response:
{
    success: true,
    build: {
        cpu: {name: "Intel i5...", price: 250},
        gpu: {name: "RTX 4060 Ti", price: 400},
        ...
    },
    total_price: 1110,
    suggestions: [...],
    validation: {
        compatible: true,
        warnings: []
    }
}
         ↓
JavaScript displays:
- Component cards with prices
- Total cost breakdown
- Compatibility status
- AI suggestions
```

---

## 6. ERROR HANDLING

### Try-Catch Pattern

```python
@builder_bp.route('/validate', methods=['POST'])
def validate_build():
    """Validate PC build compatibility."""
    try:
        # Parse request
        engine = _get_compatibility_engine()
        data = request.json or {}
        
        # Call service
        result = engine.validate_build(
            cpu_id=data.get('cpu_id'),
            motherboard_id=data.get('motherboard_id'),
            ...
        )
        
        # Return success response
        return jsonify(result), 200
        
    except ValueError as e:
        # Handle validation errors
        logger.error(f"Validation error: {e}")
        return jsonify({'error': str(e), 'success': False}), 400
        
    except Exception as e:
        # Handle unexpected errors
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return jsonify({'error': 'Server error', 'success': False}), 500
```

### Global Error Handlers

```python
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Server error'}), 500
```

---

## 7. KEY DESIGN PATTERNS

### 1. **Service Locator Pattern**
```python
# Lazy loading of services to reduce startup time
def _get_part_service():
    from server.services.part_service import PartService
    return PartService()

# Services are only loaded when needed
service = _get_part_service()
```

### 2. **Context Manager Pattern**
```python
# Automatic resource management
with get_db() as conn:
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    # Automatic commit/rollback and close
```

### 3. **Blueprint Pattern**
```python
# Modular route organization
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    pass

app.register_blueprint(auth_bp)  # Register routes
```

### 4. **Factory Pattern**
```python
# Create components based on type
def create_component(component_type, **kwargs):
    if component_type == 'cpu':
        return CPU(**kwargs)
    elif component_type == 'gpu':
        return GPU(**kwargs)
    ...
```

---

## 8. PERFORMANCE CONSIDERATIONS

### Database Optimization

```python
# ❌ Inefficient - Multiple separate queries
cpu = query_cpu(cpu_id)
gpu = query_gpu(gpu_id)
mobo = query_motherboard(mobo_id)
# 3 database round-trips

# ✅ Efficient - Single query with joins
build = query_build_with_components(build_id)
# 1 database query
```

### Caching

```python
class AIBuildService:
    _build_cache = {}  # In-memory cache
    _cache_timeout = 3600  # 1 hour
    
    # Cache repeated AI suggestions
    cache_key = f"{domain}_{budget}_{game}"
    
    if cache_key in _build_cache:
        cached_data, timestamp = _build_cache[cache_key]
        if time.time() - timestamp < _cache_timeout:
            return cached_data  # Avoid expensive computation
    
    # Compute and cache
    result = expensive_computation()
    _build_cache[cache_key] = (result, time.time())
    return result
```

### Lazy Loading

```python
# Load heavy modules only when needed
def _get_ml_service():
    from server.services.ml_build_recommender import MLBuildRecommender
    return MLBuildRecommender()

# ML service only loaded if /api/ml/* endpoint is called
```

---

## 9. SUMMARY

**Backend Architecture:**
- **Framework:** Flask (lightweight, modular)
- **Database:** SQLite (file-based, no external server)
- **Structure:** Layered (Routes → Services → Database)
- **Design Patterns:** Blueprints, context managers, service locators
- **Error Handling:** Comprehensive try-catch with logging
- **Performance:** Lazy loading, caching, optimized queries

**Request Flow:**
1. Frontend sends HTTP request
2. Flask routing layer receives request
3. Route handler validates input
4. Service layer processes business logic
5. Database layer queries/updates data
6. Response is serialized to JSON
7. Frontend receives and renders response

