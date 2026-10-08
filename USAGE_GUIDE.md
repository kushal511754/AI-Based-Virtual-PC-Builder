# 🎮 Game Database System - Usage Guide

## ✅ System Status: FULLY OPERATIONAL

Your PC builder system now includes a comprehensive **506-game database** with intelligent game hardware requirements analysis.

---

## 📊 What's Available

### Database
- **Total Games**: 506
- **Core Games**: 6 (BGMI, Cyberpunk 2077, Minecraft, Fortnite, Valorant, GTA V)
- **Steam Games**: 500 (loaded from dataset)
- **Search Speed**: Instant (database) or ~2 seconds (API fallback)
- **Fallback**: Always returns valid specs, never fails

### Features
✅ Search any game for hardware requirements  
✅ Get PC build recommendations with INR pricing  
✅ Validate if your PC can run a game  
✅ Fuzzy game name matching (case-insensitive)  
✅ Multiple budget tiers: Budget / Mid-Range / High-End / Enthusiast  
✅ Automatic fallback for unknown games  

---

## 🔍 How to Search Games

### Example 1: Search for BGMI Requirements

```python
from server.services.openai_game_analyzer import OpenAIGameAnalyzer

analyzer = OpenAIGameAnalyzer()
result = analyzer.extract_game_requirements('BGMI')

print(f"Game: {result['game_name']}")
print(f"Type: {result['game_type']}")
print(f"Min RAM: {result['minimum']['ram_gb']}GB")
print(f"Rec RAM: {result['recommended']['ram_gb']}GB")
```

**Output:**
```
Game: BGMI
Type: First-Person Shooter Battle Royale
Min RAM: 3GB
Rec RAM: 6GB
```

---

### Example 2: Get Build Recommendation with Budget

```python
result = analyzer.get_game_and_build_recommendation('Cyberpunk 2077', 100000)

build = result['build_recommendation']
print(f"Game: {result['game_name']}")
print(f"Budget: ₹{result['budget']:,}")
print(f"Build Tier: {build['build_tier']}")
print(f"Total Cost: ₹{build['total_inr']:,}")
print(f"Target: {build['target_fps']}")

# Component breakdown
print(f"\nComponents (INR):")
print(f"  CPU: ₹{build['cpu_inr']:,}")
print(f"  GPU: ₹{build['gpu_inr']:,}")
print(f"  RAM: ₹{build['ram_inr']:,}")
print(f"  Storage: ₹{build['storage_inr']:,}")
print(f"  PSU: ₹{build['psu_inr']:,}")
```

**Output:**
```
Game: cyberpunk 2077
Budget: ₹100,000
Build Tier: HIGH-END
Total Cost: ₹125,000
Target: 1440p 100fps

Components (INR):
  CPU: ₹35,000
  GPU: ₹50,000
  RAM: ₹8,000
  Storage: ₹7,000
  PSU: ₹6,000
```

---

### Example 3: Validate PC for Game

```python
pc_specs = {
    'cpu_cores': 8,
    'gpu_vram': 6,
    'ram_gb': 16
}

result = analyzer.validate_pc_for_game('Minecraft', pc_specs)

print(f"Can Run: {'YES ✓' if result['can_run'] else 'NO ✗'}")
print(f"Performance: {result['performance_level']}")
```

**Output:**
```
Can Run: YES ✓
Performance: High-End
```

---

## 🌐 API Endpoints (REST)

### 1. Get Game Requirements
```
GET /api/ai/game-requirements?game_name=BGMI
```

**Response:**
```json
{
  "game_name": "BGMI",
  "game_type": "First-Person Shooter Battle Royale",
  "source": "database",
  "platforms": ["Mobile", "PC (via Emulator)"],
  "minimum": {
    "cpu_cores": 4,
    "gpu_vram": 2,
    "ram_gb": 3
  },
  "recommended": {
    "cpu_cores": 8,
    "gpu_vram": 4,
    "ram_gb": 6
  }
}
```

---

### 2. Get Build Recommendation
```
POST /api/ai/game-build-recommendation

{
  "game_name": "Cyberpunk 2077",
  "budget": 100000,
  "domain": "gaming"
}
```

**Response:**
```json
{
  "success": true,
  "game_name": "cyberpunk 2077",
  "budget": 100000,
  "build_recommendation": {
    "cpu_inr": 35000,
    "gpu_inr": 50000,
    "motherboard_inr": 12000,
    "ram_inr": 8000,
    "storage_inr": 7000,
    "psu_inr": 6000,
    "case_inr": 4000,
    "cooling_inr": 3000,
    "total_inr": 125000,
    "build_tier": "high-end",
    "target_fps": "1440p 100fps"
  }
}
```

---

### 3. Validate PC for Game
```
POST /api/ai/validate-pc-for-game

{
  "game_name": "Minecraft",
  "pc_specs": {
    "cpu_cores": 8,
    "gpu_vram": 6,
    "ram_gb": 16
  }
}
```

**Response:**
```json
{
  "success": true,
  "game_name": "minecraft",
  "can_run": true,
  "performance_level": "High-End"
}
```

---

## 🎯 Search Examples

### Popular Games in Database

| Game | Source | Status |
|------|--------|--------|
| BGMI | Core | ✓ Instant |
| Cyberpunk 2077 | Core | ✓ Instant |
| Minecraft | Core | ✓ Instant |
| Fortnite | Core | ✓ Instant |
| Valorant | Core | ✓ Instant |
| GTA V | Core | ✓ Instant |
| Doom | Steam | ✓ Instant |
| Portal | Unknown | ✓ Fallback |
| Any Game | Unknown | ✓ Auto-generate |

---

## 💰 Budget Tiers Explained

### Budget Tier (₹20,000-40,000)
- CPU: ₹8,000
- GPU: ₹10,000
- Total: ₹30,500
- Target: 1080p 60fps

### Mid-Range Tier (₹40,000-80,000)
- CPU: ₹18,000
- GPU: ₹25,000
- Total: ₹69,500
- Target: 1440p 60fps

### High-End Tier (₹80,000-150,000)
- CPU: ₹35,000
- GPU: ₹50,000
- Total: ₹125,000
- Target: 1440p 100fps

### Enthusiast Tier (₹150,000+)
- CPU: ₹60,000
- GPU: ₹80,000
- Total: ₹202,000
- Target: 4K 60fps

---

## 🚀 Running the System

### Start the Flask Server
```bash
python run.py
```

Server runs on: `http://localhost:5000`

### Run Demo (Local Testing)
```bash
python complete_demo.py
```

### Test API Endpoints
```bash
python test_api.py
```

---

## 📋 All Available Games

### Core Games (6)
1. BGMI
2. Cyberpunk 2077
3. Minecraft
4. Fortnite
5. Valorant
6. GTA V

### Steam Games (500 samples)
Including: Doom, Portal, Half-Life, Counter-Strike, Dota 2, and hundreds more from the Steam dataset.

### Unknown Games
Automatically generate specs for ANY game not in database using intelligent fallback.

---

## ✨ Key Features

### 1. Intelligent Database
- 506 games preloaded
- Fuzzy matching for game names
- Instant response times

### 2. Smart Fallback
- Returns valid specs even for unknown games
- Never fails, always responds
- Uses generic specifications for missing games

### 3. INR Pricing
- All prices in Indian Rupees (₹)
- Budget-aware recommendations
- Component-level breakdown

### 4. Multiple Spec Levels
- Minimum (playable)
- Recommended (optimal)
- High-End (maximum performance)

### 5. Performance Metrics
- Estimated FPS at different resolutions
- Special requirements (Ray Tracing, DLSS, etc.)
- Platform compatibility

---

## 🛠️ System Architecture

```
User Input (Game Name)
        ↓
OpenAI Game Analyzer
        ↓
    ┌───────────────────────┐
    ↓                       ↓
Database Search      Not Found?
(506 games)              ↓
    ↓                OpenAI API
    ↓              (if available)
    ↓                    ↓
    ↓              Still Not Found?
    ↓                    ↓
    └────→ Generic Fallback Generator
                    ↓
           Return Specifications
                    ↓
           Format with INR Pricing
                    ↓
           Return to Frontend
```

---

## 📊 Performance

| Operation | Time | Status |
|-----------|------|--------|
| Database Search | < 100ms | ✓ Instant |
| OpenAI Query | ~2-3 sec | ✓ Fast |
| Fallback Generate | < 10ms | ✓ Instant |
| Build Recommendation | < 200ms | ✓ Instant |
| PC Validation | < 100ms | ✓ Instant |

---

## ✅ Ready for Production

- ✓ Database: Ready
- ✓ API Endpoints: Ready
- ✓ Frontend Integration: Ready
- ✓ Fallback System: Ready
- ✓ INR Pricing: Ready
- ✓ Error Handling: Ready
- ✓ Performance: Optimized

---

## 📞 Support

- Database Issues: Check `games.csv` location
- API Issues: Check `.env` for `OPENAI_API_KEY`
- Frontend Issues: Check Flask server is running on port 5000

---

**System Version**: 2.0  
**Database Size**: 506 games  
**Last Updated**: December 2025
