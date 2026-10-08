# 🏗️ PC Builder System Architecture

## High-Level System Architecture Block Diagram

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                            CLIENT LAYER (Frontend)                            │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                                │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────────────┐  │
│  │   Login Page     │  │   Home Page      │  │  PC Builder Interface    │  │
│  │ (login.html)     │  │ (home.html)      │  │  (Multiple Modes)        │  │
│  └────────┬─────────┘  └────────┬─────────┘  └──────┬───────────────────┘  │
│           │                     │                   │                       │
│  ┌────────▼──────────────────┬──▼──────────────────┬▼────────────────────┐  │
│  │    JS Controllers & Logic   │                                          │  │
│  │  ├─ builder.js             │  HTML Templates + CSS                    │  │
│  │  ├─ ai-suggestions.js      │  ├─ Manual Builder (builder.html)        │  │
│  │  ├─ search.js              │  ├─ AI Builder (ai-*.html)               │  │
│  │  └─ form-handlers.js       │  ├─ 3D Builder (3d-builder.html)         │  │
│  │                            │  ├─ Performance Analysis                  │  │
│  │    Static Assets           │  └─ Saved Builds                          │  │
│  │  ├─ animations.css         │                                          │  │
│  │  └─ styles.css             │                                          │  │
│  └────────┬──────────────────────────────────────────┬──────────────────┘  │
│           │                                          │                      │
│           └──────────────────┬───────────────────────┘                      │
│                              │                                              │
└──────────────────────────────┼──────────────────────────────────────────────┘
                               │ HTTP/JSON
                               │ REST API Calls
                               ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                      BACKEND LAYER (Flask Server)                             │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                                │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │                      ROUTING LAYER (Flask Routes)                       │ │
│  ├─────────────────────────────────────────────────────────────────────────┤ │
│  │                                                                         │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                │ │
│  │  │ auth.py      │  │ builder.py   │  │ parts.py     │                │ │
│  │  ├──────────────┤  ├──────────────┤  ├──────────────┤                │ │
│  │  │ /login       │  │ /save-build  │  │ /api/parts/* │                │ │
│  │  │ /signup      │  │ /get-builds  │  │ Components   │                │ │
│  │  │ /register    │  │ /delete-build│  │ Endpoints    │                │ │
│  │  └──────────────┘  └──────────────┘  └──────────────┘                │ │
│  │                                                                         │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                │ │
│  │  │ ai_build.py  │  │ compatibility│  │ search.py    │                │ │
│  │  ├──────────────┤  ├──────────────┤  ├──────────────┤                │ │
│  │  │ /ai/suggest  │  │ /validate    │  │ /search      │                │ │
│  │  │ /ai/domains  │  │ /check       │  │ Component    │                │ │
│  │  │ AI endpoints │  │ Compatibility│  │ Search       │                │ │
│  │  └──────────────┘  └──────────────┘  └──────────────┘                │ │
│  │                                                                         │ │
│  │  ┌──────────────┐  ┌──────────────┐                                   │ │
│  │  │ game_search  │  │ ml_routes.py │                                   │ │
│  │  ├──────────────┤  ├──────────────┤                                   │ │
│  │  │ Game search  │  │ ML Models    │                                   │ │
│  │  │ Endpoints    │  │ Endpoints    │                                   │ │
│  │  └──────────────┘  └──────────────┘                                   │ │
│  │                                                                         │ │
│  └──────────────────────────────────┬──────────────────────────────────────┘ │
│                                      │                                        │
│  ┌───────────────────────────────────▼──────────────────────────────────┐   │
│  │                      SERVICE LAYER (Business Logic)                  │   │
│  ├──────────────────────────────────────────────────────────────────────┤   │
│  │                                                                      │   │
│  │  ┌──────────────────────┐  ┌────────────────────────────────────┐  │   │
│  │  │ part_service.py      │  │ compatibility_engine.py            │  │   │
│  │  ├──────────────────────┤  ├────────────────────────────────────┤  │   │
│  │  │ - Get all parts      │  │ - CPU↔Motherboard socket check    │  │   │
│  │  │ - Filter components  │  │ - RAM↔Motherboard validation      │  │   │
│  │  │ - Search parts       │  │ - GPU power requirements          │  │   │
│  │  │ - Part suggestions   │  │ - Case physical fit checks        │  │   │
│  │  │ - Price lookups      │  │ - PSU wattage validation          │  │   │
│  │  │ - Stock checks       │  │ - Cooling solution TDP checks     │  │   │
│  │  └──────────────────────┘  └────────────────────────────────────┘  │   │
│  │                                                                      │   │
│  │  ┌──────────────────────┐  ┌────────────────────────────────────┐  │   │
│  │  │ ai_build_service.py  │  │ pc_build_agent.py                  │  │   │
│  │  ├──────────────────────┤  ├────────────────────────────────────┤  │   │
│  │  │ - AI suggestions     │  │ - Real component selection         │  │   │
│  │  │ - Domain selection   │  │ - Budget validation                │  │   │
│  │  │ - Budget handling    │  │ - Retailer sourcing               │  │   │
│  │  │ - Suggestion ranking │  │ - Price aggregation               │  │   │
│  │  └──────────────────────┘  └────────────────────────────────────┘  │   │
│  │                                                                      │   │
│  │  ┌──────────────────────┐  ┌────────────────────────────────────┐  │   │
│  │  │ build_service.py     │  │ pricing_service.py                 │  │   │
│  │  ├──────────────────────┤  ├────────────────────────────────────┤  │   │
│  │  │ - Save builds        │  │ - Calculate totals                 │  │   │
│  │  │ - Load builds        │  │ - Price breakdown                  │  │   │
│  │  │ - Edit builds        │  │ - Cost per performance             │  │   │
│  │  │ - Delete builds      │  │ - Bottleneck detection             │  │   │
│  │  │ - Build history      │  │ - Upgrade suggestions              │  │   │
│  │  └──────────────────────┘  └────────────────────────────────────┘  │   │
│  │                                                                      │   │
│  │  ┌──────────────────────┐  ┌────────────────────────────────────┐  │   │
│  │  │ ml_build_recommender │  │ game_database_service.py           │  │   │
│  │  ├──────────────────────┤  ├────────────────────────────────────┤  │   │
│  │  │ - ML predictions     │  │ - Game requirements lookup         │  │   │
│  │  │ - Pattern matching   │  │ - Performance tiers                │  │   │
│  │  │ - Training logic     │  │ - Genre mapping                    │  │   │
│  │  └──────────────────────┘  └────────────────────────────────────┘  │   │
│  │                                                                      │   │
│  │  ┌──────────────────────┐  ┌────────────────────────────────────┐  │   │
│  │  │ openai_game_analyzer │  │ realtime_component_fetcher.py      │  │   │
│  │  ├──────────────────────┤  ├────────────────────────────────────┤  │   │
│  │  │ - OpenAI integration │  │ - Real-time pricing                │  │   │
│  │  │ - Game analysis      │  │ - Stock availability               │  │   │
│  │  │ - NLP processing     │  │ - Retailer updates                 │  │   │
│  │  └──────────────────────┘  └────────────────────────────────────┘  │   │
│  │                                                                      │   │
│  └──────────────────────────────────┬───────────────────────────────────┘   │
│                                      │                                        │
│  ┌───────────────────────────────────▼──────────────────────────────────┐   │
│  │                  DATABASE & UTILITIES LAYER                         │   │
│  ├──────────────────────────────────────────────────────────────────────┤   │
│  │                                                                      │   │
│  │  ┌──────────────────────────────────────────────────────────────┐  │   │
│  │  │ SQLite Database (database.db)                                │  │   │
│  │  ├──────────────────────────────────────────────────────────────┤  │   │
│  │  │ Tables:                                                      │  │   │
│  │  │ ├─ users (Authentication)                                   │  │   │
│  │  │ ├─ cpu, gpu, motherboard, ram, storage, psu, case, cooling │  │   │
│  │  │ ├─ saved_build (User's saved builds)                        │  │   │
│  │  │ ├─ domain_requirements (Performance benchmarks)             │  │   │
│  │  │ ├─ game_requirements (Game specifications)                  │  │   │
│  │  │ └─ ai_build_history (AI suggestion history)                 │  │   │
│  │  └──────────────────────────────────────────────────────────────┘  │   │
│  │                                                                      │   │
│  │  ┌──────────────────────────────────────────────────────────────┐  │   │
│  │  │ db.py (Database Connection & Initialization)                │  │   │
│  │  │ ├─ get_db() - Context manager for DB connections           │  │   │
│  │  │ ├─ init_db() - Create tables on startup                    │  │   │
│  │  │ └─ dict_from_row() - Convert DB rows to dictionaries       │  │   │
│  │  └──────────────────────────────────────────────────────────────┘  │   │
│  │                                                                      │   │
│  │  ┌──────────────────────────────────────────────────────────────┐  │   │
│  │  │ helpers.py (Utility Functions)                               │  │   │
│  │  │ ├─ Validation helpers                                        │  │   │
│  │  │ ├─ Formatting utilities                                      │  │   │
│  │  │ ├─ Calculation functions                                     │  │   │
│  │  │ └─ Error handling                                            │  │   │
│  │  └──────────────────────────────────────────────────────────────┘  │   │
│  │                                                                      │   │
│  └──────────────────────────────────┬───────────────────────────────────┘   │
│                                      │                                        │
└──────────────────────────────────────┼────────────────────────────────────────┘
                                       │
                                       ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                    EXTERNAL SERVICES & APIs LAYER                             │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                                │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────────────┐   │
│  │  OpenAI API      │  │ Retailer APIs    │  │  ML Model Storage        │   │
│  ├──────────────────┤  ├──────────────────┤  ├──────────────────────────┤   │
│  │ Game analysis    │  │ Real-time prices │  │ Trained models           │   │
│  │ NLP processing   │  │ Stock updates    │  │ Feature extractors       │   │
│  │ Budget planning   │  │ Component data   │  │ Predictions              │   │
│  └──────────────────┘  └──────────────────┘  └──────────────────────────┘   │
│                                                                                │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 📊 Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER REQUEST FLOW                            │
└──────────────────────────────────────────────────────────────────────┘

1. LOGIN FLOW
═════════════════════════════════════════════════════════════════════

User Input (login.html)
    ↓
POST /api/auth/login
    ↓
auth.py (Route Handler)
    ↓
auth.py (Login Endpoint)
    ↓
SQLite: Check users table
    ↓
Response with JWT/Session
    ↓
Redirect to /home
    ↓
home.html (Dashboard)


2. PC BUILDER FLOW (Manual)
═════════════════════════════════════════════════════════════════════

User selects components (builder.html)
    ↓
GET /api/parts/cpu, /api/parts/gpu, etc.
    ↓
parts.py (Route Handler)
    ↓
part_service.py (Business Logic)
    ↓
SQLite: Query from component tables
    ↓
Response with component lists
    ↓
UI displays options
    ↓
User clicks "Check Compatibility"
    ↓
POST /api/build/validate
    ↓
compatibility.py (Route Handler)
    ↓
compatibility_engine.py (Validation Logic)
    ↓
Multiple checks (socket, RAM, power, fit, cooling)
    ↓
Response with validation results
    ↓
UI displays compatibility warnings/errors
    ↓
User clicks "Save Build"
    ↓
POST /api/build/save
    ↓
builder.py (Route Handler)
    ↓
build_service.py (Save Logic)
    ↓
SQLite: Insert into saved_build table
    ↓
Build saved successfully


3. AI BUILDER FLOW
═════════════════════════════════════════════════════════════════════

User selects domain (ai-domain-selection.html)
    ↓
User enters budget & game (ai-game-input.html)
    ↓
POST /api/ai/suggest-build
    ↓
ai_build.py (Route Handler)
    ↓
ai_build_service.py (Service Layer)
    ↓
├─→ pc_build_agent.py (Component Selection)
│   ├─ Validate budget
│   ├─ Query retailer APIs
│   ├─ Select components
│   └─ Calculate total
│
├─→ compatibility_engine.py (Validation)
│   └─ Verify all components work together
│
└─→ pricing_service.py (Price Analysis)
    └─ Calculate breakdown & suggestions

Response with suggested build
    ↓
ai-suggestions.html (Display)
    ↓
Display components with prices
    ↓
User clicks "Save Build" or "Refine"


4. SEARCH FLOW
═════════════════════════════════════════════════════════════════════

User types in search (search.html)
    ↓
GET /api/search?q=query
    ↓
search.py (Route Handler)
    ↓
AI component search service
    ↓
SQLite: Query with filters
    ↓
ML ranking (if available)
    ↓
Response with ranked results
    ↓
UI displays search results
    ↓
User selects result or refines search
```

---

## 🔄 Component Interaction Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                   CORE COMPONENTS & DEPENDENCIES                │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────────┐
│   Routes Layer       │
│   (API Endpoints)    │
├──────────────────────┤
│ ├─ auth.py           │
│ ├─ builder.py        │ ───────────┐
│ ├─ parts.py          │            │ All routes delegate
│ ├─ ai_build.py       │            │ to services
│ ├─ compatibility.py  │ ───────────┤
│ ├─ search.py         │            │
│ ├─ games.py          │            │
│ └─ ml_routes.py      │            │
└──────────┬───────────┘            │
           │                        │
           ▼                        ▼
┌─────────────────────────────────────────────┐
│      Services Layer (Business Logic)         │
├──────────────────────────────────────────────┤
│                                              │
│  ┌─────────────────────────────────────┐   │
│  │ part_service.py                     │   │
│  │ - Component CRUD & filtering        │   │
│  └──────────┬──────────────────────────┘   │
│             │                              │
│  ┌──────────▼──────────────────────────┐   │
│  │ compatibility_engine.py              │   │
│  │ - Multi-layer validation             │   │
│  │ - Error reporting                    │   │
│  └──────────┬──────────────────────────┘   │
│             │                              │
│  ┌──────────▼──────────────────────────┐   │
│  │ ai_build_service.py                  │   │
│  │ - Orchestrates AI suggestions       │   │
│  │ - Calls pc_build_agent              │   │
│  │ - Validates & formats response      │   │
│  └──────────┬──────────────────────────┘   │
│             │                              │
│  ┌──────────▼──────────────────────────┐   │
│  │ build_service.py                     │   │
│  │ - Saves/loads/deletes builds        │   │
│  └──────────┬──────────────────────────┘   │
│             │                              │
│  ┌──────────▼──────────────────────────┐   │
│  │ pricing_service.py                   │   │
│  │ - Price calculations & analysis     │   │
│  └──────────┬──────────────────────────┘   │
│             │                              │
│  ┌──────────▼──────────────────────────┐   │
│  │ game_database_service.py             │   │
│  │ - Game specs lookup                 │   │
│  └──────────┬──────────────────────────┘   │
│             │                              │
│  ┌──────────▼──────────────────────────┐   │
│  │ ml_build_recommender.py              │   │
│  │ - ML-based suggestions              │   │
│  └──────────┬──────────────────────────┘   │
│             │                              │
└─────────────┼──────────────────────────────┘
              │
              ▼
┌──────────────────────────────────────┐
│  Database Utilities & Models         │
├──────────────────────────────────────┤
│ ├─ db.py (Connection & Init)         │
│ ├─ helpers.py (Utility functions)    │
│ └─ models/ (Data models)             │
└──────────┬───────────────────────────┘
           │
           ▼
┌──────────────────────────────────────┐
│   SQLite Database (database.db)      │
├──────────────────────────────────────┤
│ ├─ users (Auth)                      │
│ ├─ Component tables                  │
│ │  (cpu, gpu, ram, etc.)             │
│ ├─ saved_build (Persistence)         │
│ ├─ Requirements tables                │
│ └─ History tables                    │
└──────────────────────────────────────┘
```

---

## 🎯 Key Features Architecture

```
╔════════════════════════════════════════════════════════════════════╗
║              FEATURE-BASED COMPONENT MAPPING                        ║
╚════════════════════════════════════════════════════════════════════╝

┌─ AUTHENTICATION ──────────────────────────────────────┐
│ Routes:  auth.py                                       │
│ Service: (Built into routes)                          │
│ DB:      users table                                  │
│ UI:      login.html, signup.html                      │
└───────────────────────────────────────────────────────┘

┌─ COMPONENT BROWSING ──────────────────────────────────┐
│ Routes:  parts.py, quick_parts.py                     │
│ Service: part_service.py                              │
│ DB:      cpu, gpu, motherboard, ram, storage, psu,   │
│          pc_case, cooling tables                      │
│ UI:      builder.html, component selection dropdowns │
└───────────────────────────────────────────────────────┘

┌─ COMPATIBILITY CHECKING ──────────────────────────────┐
│ Routes:  compatibility.py                             │
│ Service: compatibility_engine.py                      │
│ DB:      All component tables                         │
│ UI:      Real-time validation display                │
│ Checks:  Socket, RAM type, Power, Physical fit, TDP │
└───────────────────────────────────────────────────────┘

┌─ MANUAL PC BUILDING ──────────────────────────────────┐
│ Routes:  builder.py                                   │
│ Service: build_service.py                            │
│ DB:      saved_build table                           │
│ UI:      builder.html, manual-builder.html           │
│ Features: Drag-drop, form-based selection            │
└───────────────────────────────────────────────────────┘

┌─ AI-POWERED BUILDING ─────────────────────────────────┐
│ Routes:  ai_build.py                                 │
│ Service: ai_build_service.py, pc_build_agent.py      │
│ DB:      All tables, domain_requirements             │
│ UI:      ai-domain-selection.html, ai-game-input.html│
│          ai-suggestions.html                         │
│ Features: Budget-based, game-based, domain selection │
└───────────────────────────────────────────────────────┘

┌─ PRICING & ANALYSIS ──────────────────────────────────┐
│ Routes:  builder.py, ai_build.py                     │
│ Service: pricing_service.py                          │
│ DB:      All component tables                        │
│ UI:      Price breakdown, cost analysis              │
│ Features: Total, per-component, performance ratio    │
└───────────────────────────────────────────────────────┘

┌─ SEARCH & FILTERING ──────────────────────────────────┐
│ Routes:  search.py, game_search.py                   │
│ Service: Multiple search services                    │
│ DB:      All component tables, game_requirements     │
│ UI:      search.html, game_search.html               │
│ Features: Text search, ML ranking, filters           │
└───────────────────────────────────────────────────────┘

┌─ ML & AI ANALYSIS ────────────────────────────────────┐
│ Routes:  ml_routes.py                                │
│ Service: ml_build_recommender.py,                    │
│          ml_game_classifier.py,                      │
│          ml_price_predictor.py,                      │
│          openai_game_analyzer.py                     │
│ DB:      All tables + ai_build_history               │
│ UI:      ML prediction displays                      │
│ Features: Recommendations, game analysis, pricing    │
└───────────────────────────────────────────────────────┘

┌─ PERFORMANCE ANALYSIS ────────────────────────────────┐
│ Routes:  builder.py, ai_build.py                     │
│ Service: Multiple services                           │
│ DB:      domain_requirements, game_requirements      │
│ UI:      performance-analysis.html                   │
│ Features: FPS estimates, bottleneck detection        │
└───────────────────────────────────────────────────────┘

┌─ BUILD PERSISTENCE ───────────────────────────────────┐
│ Routes:  builder.py                                   │
│ Service: build_service.py                            │
│ DB:      saved_build table                           │
│ UI:      saved.html                                  │
│ Features: Save, load, edit, delete, view history     │
└───────────────────────────────────────────────────────┘
```

---

## 📈 Scaling & Performance

```
CURRENT ARCHITECTURE BOTTLENECKS & SOLUTIONS:

┌─ Database Queries ────────────────────────────────────┐
│ Issue: Multiple component queries per request         │
│ Solution: Query optimization, caching, indexing       │
└───────────────────────────────────────────────────────┘

┌─ Component Selection ─────────────────────────────────┐
│ Issue: Large component database (500+ items)          │
│ Solution: ML ranking, client-side filtering          │
└───────────────────────────────────────────────────────┘

┌─ AI Requests ─────────────────────────────────────────┐
│ Issue: OpenAI API calls are slow                      │
│ Solution: Caching, async processing, local fallback   │
└───────────────────────────────────────────────────────┘

┌─ Real-time Price Updates ─────────────────────────────┐
│ Issue: Retailer APIs may be slow                      │
│ Solution: Background jobs, caching, fallback prices   │
└───────────────────────────────────────────────────────┘

FUTURE SCALING ROADMAP:

├─ PostgreSQL migration (for larger datasets)
├─ Redis caching layer
├─ Async task queue (Celery)
├─ Microservices (separate AI, pricing, search)
├─ CDN for static assets
├─ API rate limiting & authentication
├─ Database sharding for components
└─ ML model versioning & deployment
```

---

## 🔐 Security Architecture

```
┌──────────────────────────────────────────────────────────┐
│              SECURITY LAYERS                             │
├──────────────────────────────────────────────────────────┤
│                                                          │
│ 1. AUTHENTICATION                                        │
│    ├─ User login/signup via /api/auth/                  │
│    ├─ Password hashing (SHA256)                         │
│    ├─ Session management                               │
│    └─ User data in localStorage                        │
│                                                          │
│ 2. INPUT VALIDATION                                      │
│    ├─ Route-level validation                           │
│    ├─ Service-level checks                             │
│    ├─ Budget constraints validation                    │
│    └─ Component compatibility rules                    │
│                                                          │
│ 3. ERROR HANDLING                                        │
│    ├─ Try-catch blocks                                  │
│    ├─ Graceful fallbacks                                │
│    ├─ Error logging                                     │
│    └─ User-friendly error messages                     │
│                                                          │
│ 4. DATABASE SECURITY                                     │
│    ├─ SQLite (local, no network exposure)              │
│    ├─ Parameterized queries                             │
│    ├─ Connection pooling                                │
│    └─ Data validation before insert                    │
│                                                          │
│ 5. API SECURITY                                          │
│    ├─ Input sanitization                                │
│    ├─ CORS headers                                       │
│    ├─ Rate limiting (future)                           │
│    └─ Request validation                                │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## 📦 Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              DEPLOYMENT CONFIGURATIONS                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ DEVELOPMENT (Local)                                        │
│ ├─ Flask development server (port 5000)                   │
│ ├─ SQLite database (single file)                          │
│ ├─ Console logging                                        │
│ └─ Hot reload enabled                                     │
│                                                             │
│ PRODUCTION (Heroku/Render)                                │
│ ├─ Gunicorn WSGI server                                   │
│ ├─ SQLite database (persistent volume)                    │
│ ├─ Environment variables (.env)                           │
│ ├─ Error logging to files                                 │
│ ├─ Procfile configuration                                 │
│ └─ Runtime specifications                                 │
│                                                             │
│ DOCKER (Future)                                            │
│ ├─ Containerized Flask app                                │
│ ├─ PostgreSQL container                                   │
│ ├─ Redis cache container                                  │
│ ├─ Volume management                                       │
│ └─ Multi-stage builds                                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎨 Technology Stack Summary

```
┌───────────────────────────────────────────────────────────┐
│                   TECHNOLOGY STACK                        │
├───────────────────────────────────────────────────────────┤
│                                                           │
│ BACKEND                                                   │
│ ├─ Runtime:      Python 3.10+                            │
│ ├─ Framework:    Flask 2.3.3                             │
│ ├─ Database:     SQLite3                                 │
│ ├─ WSGI Server:  Gunicorn (production)                   │
│ ├─ AI/ML:        OpenAI API, scikit-learn                │
│ ├─ ML Library:   TensorFlow, sentence-transformers       │
│ └─ Utilities:    Python-dotenv, requests, numpy, scipy   │
│                                                           │
│ FRONTEND                                                  │
│ ├─ Markup:       HTML5                                   │
│ ├─ Styling:      CSS3, animations                        │
│ ├─ Scripts:      Vanilla JavaScript (ES6+)               │
│ ├─ DOM:          Fetch API, async/await                  │
│ ├─ Local Storage: For session persistence                │
│ └─ Media:        SVG, images, icons                      │
│                                                           │
│ INFRASTRUCTURE                                            │
│ ├─ Hosting:      Heroku, Render (PaaS)                   │
│ ├─ Version Control: Git                                  │
│ ├─ Package Manager: pip                                  │
│ ├─ Virtual Env:  venv                                    │
│ └─ Config:       Environment variables                   │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

