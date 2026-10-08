# AIPCSimulator - Quick Start Guide

## 🚀 Getting Started in 60 Seconds

### Step 1: Install Dependencies
```bash
cd c:\Users\LEENOVO\Desktop\projectk
pip install -r requirements.txt
```

### Step 2: Populate Database (if not done)
```bash
python populate_db.py
```

### Step 3: Run the Application
```bash
python run.py
```

### Step 4: Open in Browser
Navigate to: **http://localhost:5000**

---

## 🎯 Using the App

### Home Page
- View features and component counts
- Click "Start Building" to go to the PC Builder

### PC Builder (`/builder`)
1. **Select CPU** → Choose a processor (must have)
2. **Select Motherboard** → Must match CPU socket (must have)
3. **Add Optional Components**:
   - GPU (graphics card)
   - RAM (memory)
   - Storage (SSD/HDD)
   - PSU (power supply)
   - Case
   - Cooling Solution
4. **Real-Time Feedback**:
   - ✅ Compatibility status (errors and warnings)
   - 💰 Total price and breakdown
   - 💡 Smart suggestions
5. **Save Build** → Click "Save Build" to store for later

### My Builds (`/saved`)
- View all saved builds
- See detailed component specs
- Delete builds

---

## 🔍 Compatibility Rules

The system automatically checks:

| Component | Rule |
|-----------|------|
| **CPU ↔ Motherboard** | Socket types must match |
| **RAM ↔ Motherboard** | RAM type and capacity must be supported |
| **GPU ↔ PSU** | Total power draw ≤ PSU capacity |
| **GPU ↔ Case** | GPU length must fit in case |
| **Cooling ↔ CPU** | Cooler TDP must handle CPU TDP |

---

## 💻 Example Build

Try this configuration:

1. **CPU**: Intel Core i7-13700K
2. **Motherboard**: ASUS TUF Gaming X870 (wait, pick a Z790 board!)
3. **GPU**: NVIDIA RTX 4080
4. **RAM**: Corsair Vengeance DDR5 32GB
5. **Storage**: Samsung 990 Pro 2TB
6. **PSU**: Corsair RM1000x
7. **Case**: NZXT H7 Flow
8. **Cooling**: Corsair H150i Elite

**Expected Result**: ~$4,500 compatible gaming build

---

## 🛠️ Customizing Components

To add more components, edit `populate_db.py`:

```python
# Add more CPUs
cpus = [
    ('Your CPU Name', 'Socket', cores, threads, base_clock, turbo_clock, tdp, price, 'Manufacturer'),
    # ... more CPUs
]
```

Then run:
```bash
python populate_db.py
```

---

## 📊 API Testing

Use curl or Postman to test endpoints:

```bash
# Get all CPUs
curl http://localhost:5000/api/parts/cpu

# Validate build
curl -X POST http://localhost:5000/api/build/validate \
  -H "Content-Type: application/json" \
  -d '{"cpu_id": 1, "motherboard_id": 1, "gpu_id": 1}'

# Get price analysis
curl -X POST http://localhost:5000/api/build/price \
  -H "Content-Type: application/json" \
  -d '{"cpu_id": 1, "motherboard_id": 1, "gpu_id": 1}'
```

---

## 🎮 Features Explained

### Compatibility Engine
- Real-time validation as you select components
- Highlights errors (red) and warnings (yellow)
- Prevents incompatible combinations

### Pricing Service
- Component-by-component breakdown
- Total build cost calculation
- Performance tier classification
- Bottleneck detection
- Upgrade suggestions

### Smart Suggestions
- "Consider 16GB+ RAM for multitasking"
- "High-end GPU selected - ensure PSU is adequate"
- "Potential CPU bottleneck - Consider upgrading CPU"

---

## 🔧 Troubleshooting

**Q: "ModuleNotFoundError: No module named 'server'"**
- Run from project root directory: `cd c:\Users\LEENOVO\Desktop\projectk`

**Q: "Database is locked"**
- Close other Flask instances
- Delete `database.db` and run `populate_db.py` again

**Q: "Port 5000 already in use"**
- Edit `run.py` to use a different port: `app.run(port=8080)`

**Q: "Components not loading"**
- Run `python populate_db.py`
- Check that `database.db` exists

---

## 📁 Project Structure Quick Reference

```
projectk/
├── run.py                    ← START HERE
├── populate_db.py            ← Populate database
├── database.db               ← Database (auto-created)
├── server/
│   ├── app.py                ← Flask app
│   ├── routes/               ← API endpoints
│   ├── services/             ← Business logic
│   └── utils/                ← Database helpers
├── templates/                ← HTML pages
└── static/                   ← CSS & JavaScript
```

---

## 🌐 Browser Support

- Chrome/Edge: ✅ Full support
- Firefox: ✅ Full support
- Safari: ✅ Full support
- IE11: ❌ Not supported

---

## 💡 Tips & Tricks

1. **Socket Compatibility**: Select CPU first, then motherboard filters to compatible sockets
2. **Power Draw**: Total system power = CPU TDP + GPU power draw + overhead
3. **Bottleneck Detection**: Mismatched CPU/GPU power tiers trigger warnings
4. **Save Multiple Builds**: Compare different configs in My Builds
5. **Budget Builds**: Start with budget CPUs (Ryzen 5 7600X) and build from there

---

## 🚀 Next Steps

- Add more components to database
- Extend compatibility rules
- Implement 3D visualization
- Add performance benchmarking
- Export builds as JSON/PDF

---

**Happy building! 🖥️**
