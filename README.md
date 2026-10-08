# AIPCSimulator - PC Builder & Simulator Web App

A full-stack Python/Flask web application for building, configuring, and analyzing custom PC builds with compatibility checking and pricing analysis.

## Pricing policy

The legacy SQLite component catalogue stores **reference MSRP in USD**. Interfaces display those values in INR using a fixed planning rate of **₹83 per USD** and label them as reference prices, not live retailer quotes. The AI build flow uses its own INR catalogue and identifies its source in each recommendation. Prices should be verified with a retailer before purchase.

## 🚀 Features

- **Real-Time Compatibility Checking**
  - CPU ↔ Motherboard socket validation
  - RAM ↔ Motherboard type and capacity checks
  - GPU ↔ PSU power draw validation
  - GPU ↔ Case physical fit checks
  - Cooling solution ↔ CPU TDP verification

- **Smart Pricing Analysis**
  - Total build cost calculation
  - Price breakdown by component category
  - Cost-per-performance insights
  - Upgrade/downgrade suggestions
  - Bottleneck detection

- **Build Management**
  - Save and load custom builds
  - View saved builds library
  - Detailed build analysis
  - Delete saved builds

- **Component Database**
  - 110+ PC components across 8 categories (CPUs, GPUs, Motherboards, RAM, Storage, PSU, Cases, Cooling)
  - Specifications based on manufacturer data
  - Reference USD prices with an explicit INR planning conversion for display

## 📋 Project Structure

```
projectk/
├── server/                  # Backend Flask application
│   ├── app.py              # Main Flask app
│   ├── routes/             # API endpoints
│   │   ├── parts.py        # Component API routes
│   │   └── builder.py      # Build management routes
│   ├── services/           # Business logic
│   │   ├── part_service.py         # Component queries
│   │   ├── compatibility_engine.py # Compatibility checking
│   │   ├── pricing_service.py      # Price analysis
│   │   └── build_service.py        # Build persistence
│   ├── models/             # Data models
│   │   ├── cpu.py
│   │   └── gpu.py
│   └── utils/              # Database utilities
│       ├── db.py           # Database initialization & helpers
│       └── helpers.py      # Utility functions
├── templates/              # Jinja2 HTML templates
│   ├── index.html          # Homepage
│   ├── builder.html        # PC builder interface
│   ├── saved.html          # Saved builds page
│   ├── 404.html            # Error pages
│   └── 500.html
├── static/                 # Static files
│   ├── css/
│   │   └── styles.css      # Main stylesheet
│   └── js/
│       └── builder.js      # Builder JavaScript
├── database.db             # SQLite database (auto-created)
├── populate_db.py          # Database population script
├── run.py                  # Application entry point
└── requirements.txt        # Python dependencies
```

## 🗄️ Database Schema

### Tables
- **cpu**: Processor specifications
- **gpu**: Graphics card specifications
- **motherboard**: Motherboard specs with socket/RAM info
- **ram**: RAM modules with type/speed
- **storage**: SSDs and HDDs
- **psu**: Power supply units
- **pc_case**: Computer cases with size constraints
- **cooling**: CPU cooling solutions
- **saved_build**: User-saved PC configurations

## 🛠️ Technology Stack

- **Backend**: Flask 2.3.3 (Python web framework)
- **Database**: SQLite3 (no external DB needed)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **API**: RESTful JSON endpoints

## 📦 Installation & Setup

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Populate Database with Sample Components
```bash
python populate_db.py
```

This will:
- Create `database.db` file
- Initialize all tables
- Add 40+ sample PC components

### 3. Run the Application
```bash
python run.py
```

The app will start on `http://localhost:5000`

## 🌐 API Endpoints

### Components API
```
GET  /api/parts/cpu                    # Get all CPUs
GET  /api/parts/gpu                    # Get all GPUs
GET  /api/parts/motherboard            # Get all motherboards
GET  /api/parts/ram                    # Get all RAM
GET  /api/parts/storage                # Get all storage
GET  /api/parts/psu                    # Get all PSUs
GET  /api/parts/case                   # Get all cases
GET  /api/parts/cooling                # Get all cooling solutions
GET  /api/parts/cpu/<id>/compatible-motherboards
```

### Builder API
```
POST /api/build/validate               # Check build compatibility
POST /api/build/price                  # Analyze build pricing
POST /api/build/save                   # Save a build
GET  /api/build/builds                 # Get all saved builds
GET  /api/build/build/<id>             # Get build details
DELETE /api/build/build/<id>           # Delete a build
```

## 🎮 User Interface

### Pages

**1. Home Page** (`/`)
- Feature overview
- Component statistics
- Quick start button

**2. PC Builder** (`/builder`)
- Component selection dropdowns
- Real-time compatibility checking
- Price analysis panel
- Smart suggestions
- Save build functionality

**3. Saved Builds** (`/saved`)
- View all saved builds
- Detailed build information
- Delete builds

## 🔧 Compatibility Rules

The engine checks:

| Check | Rule | Action |
|-------|------|--------|
| CPU Socket | CPU socket must match motherboard socket | Error if mismatch |
| RAM Type | RAM type must match motherboard support | Error if mismatch |
| RAM Capacity | RAM size ≤ motherboard max | Error if exceeded |
| Power Draw | Total power ≤ PSU capacity - 150W | Error if insufficient |
| GPU Length | GPU length ≤ case max GPU length | Error if doesn't fit |
| PSU in Case | PSU wattage advisory check | Warning only |
| Cooling TDP | Cooler TDP ≥ CPU TDP | Warning if inadequate |

## 💰 Pricing Features

- **Component Breakdown**: See price per category
- **Bottleneck Detection**: Identify mismatched components
- **Performance Tier**: Automatic CPU/GPU classification
- **Upgrade Suggestions**: Recommendations for balanced builds
- **Cost Analysis**: Price-to-performance ratio

## 🎯 Building a PC - Step by Step

1. **Navigate to Builder** → Click "Builder" in navigation
2. **Select CPU** → Choose processor (auto-filters compatible motherboards)
3. **Select Motherboard** → Must match CPU socket
4. **Add Optional Components** → GPU, RAM, Storage, PSU, Case, Cooling
5. **Check Compatibility** → Real-time validation appears on right panel
6. **Review Pricing** → See total cost and breakdown
7. **Read Suggestions** → Get smart recommendations
8. **Save Build** → Click "Save Build" to store for later

## 📊 Sample Components Included

**CPUs**: Intel i3/i5/i7/i9, AMD Ryzen 5/7/9
**GPUs**: NVIDIA RTX 40-series, AMD Radeon RX 7000-series
**Motherboards**: Z790, B760, X870, B850, B450
**RAM**: DDR5 6000MHz, DDR4 3600MHz modules
**Storage**: NVMe SSDs, SATA SSDs, HDDs
**PSUs**: 650W-1000W with 80+ Gold/Bronze
**Cases**: ATX Mid-tower cases
**Cooling**: Air and liquid CPU coolers

## 🚀 Running on Replit

The app is optimized for Replit:
- No external dependencies needed
- SQLite database stored locally
- Auto-create database on first run
- Lightweight and fast

```bash
python run.py
```

## 📝 Configuration

All configuration is built-in. Optional customizations:

**Change Port** (in `run.py`):
```python
app.run(debug=True, host='0.0.0.0', port=8080)
```

**Enable/Disable Debug**:
```python
app.run(debug=False)  # Production mode
```

## 🐛 Troubleshooting

**"Database is locked" error**
- Close other Flask instances
- Delete `database.db` and run `populate_db.py` again

**API returns 404**
- Ensure Flask is running on `http://localhost:5000`
- Check browser console for network errors

**Components not loading**
- Run `populate_db.py` to ensure database is populated
- Check that `database.db` exists

## 🔮 Future Enhancements

- [ ] 3D PC visualization using Three.js
- [ ] Import/export builds as JSON
- [ ] Component comparison tool
- [ ] User authentication & cloud saves
- [ ] Performance benchmarking integration
- [ ] VR PC building experience
- [ ] GPU performance metrics
- [ ] Power consumption simulator

## 📄 License

This project is provided as-is for educational purposes.

## 🤝 Contributing

Feel free to add more components to `populate_db.py` or extend the compatibility rules in `compatibility_engine.py`.

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the code comments
3. Check browser console for JavaScript errors
4. Check terminal for Flask errors

---

**Build smarter. Game harder. With AIPCSimulator! 🖥️**
