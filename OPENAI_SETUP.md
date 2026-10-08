# 🎮 OpenAI Game Requirements API - Complete Guide

## Overview

Your PC builder now has **AI-powered game analysis** using OpenAI GPT! You can:

✅ Search for **ANY game** - BGMI, Cyberpunk 2077, PUBG Mobile, Fortnite, etc.
✅ Get **automatic hardware requirements** - CPU, GPU, RAM, storage recommendations
✅ Receive **AI-powered build recommendations** - Based on game needs + budget
✅ **Validate existing PCs** - Check if your PC can run any game

---

## Setup (One-time)

### 1. Set Your OpenAI API Key

```bash
# Windows PowerShell
python setup_openai.py

# Linux/Mac
python3 setup_openai.py
```

Or manually create `.env` file in project root:
```
OPENAI_API_KEY=sk-your-key-here
```

### 2. Restart the Server

```bash
python run.py
```

---

## API Endpoints

### 1️⃣ Get Game Requirements

Get hardware specifications for ANY game.

**Endpoint**: `GET /api/ai/game-requirements`

**Request**:
```bash
curl "http://localhost:5000/api/ai/game-requirements?game_name=BGMI"
```

**Request (POST)**:
```json
POST /api/ai/game-requirements
Content-Type: application/json

{
  "game_name": "BGMI"
}
```

**Response**:
```json
{
  "success": true,
  "source": "openai",
  "data": {
    "game_name": "BGMI",
    "platforms": ["Mobile", "PC (via Emulator)", "Cloud Gaming"],
    "game_type": "First-Person Shooter Battle Royale",
    "release_year": 2021,
    "minimum": {
      "cpu_cores": 4,
      "cpu_name": "Snapdragon 600 or equivalent",
      "gpu_vram": 2,
      "gpu_name": "Adreno 505 or equivalent",
      "ram_gb": 3,
      "storage_gb": 5,
      "os": "Android 5.0+"
    },
    "recommended": {
      "cpu_cores": 8,
      "cpu_name": "Snapdragon 855 or equivalent",
      "gpu_vram": 4,
      "gpu_name": "Adreno 640 or equivalent",
      "ram_gb": 6,
      "storage_gb": 10,
      "os": "Android 10+"
    },
    "high_end": {
      "cpu_cores": 12,
      "cpu_name": "Snapdragon 8 Gen 2 or equivalent",
      "gpu_vram": 8,
      "gpu_name": "Adreno 8 Gen 2 or equivalent",
      "ram_gb": 12,
      "storage_gb": 20,
      "os": "Android 13+"
    },
    "estimated_fps": {
      "1080p_high": "90-120 FPS",
      "1440p_high": "60-90 FPS",
      "4k_high": "30-60 FPS (for emulator)"
    },
    "special_requirements": ["GPU Acceleration", "Minimum 5 GB Storage"],
    "notes": "BGMI is primarily a mobile game. For PC gaming, use Android emulator like BlueStacks with these specs."
  }
}
```

---

### 2️⃣ Get Build Recommendation for Game + Budget

Get a complete PC build recommendation for a game with your budget.

**Endpoint**: `POST /api/ai/game-build-recommendation`

**Request**:
```json
{
  "game_name": "BGMI",
  "budget": 80000,
  "domain": "gaming"
}
```

**Response**:
```json
{
  "success": true,
  "game_name": "BGMI",
  "budget_inr": 80000,
  "source": "openai",
  "game_requirements": {
    "game_name": "BGMI",
    "platforms": ["Mobile", "PC (via Emulator)"],
    "minimum": {...},
    "recommended": {...}
  },
  "build_recommendation": {
    "budget_sufficient": true,
    "performance_target": "1080p 120fps Streaming",
    "recommended_cpu_tier": "Mid-range",
    "recommended_gpu_tier": "Mid-range",
    "approximate_component_costs": {
      "cpu_inr": 15000,
      "gpu_inr": 25000,
      "motherboard_inr": 8000,
      "ram_inr": 5000,
      "storage_inr": 4000,
      "psu_inr": 4000,
      "case_inr": 2500,
      "cooling_inr": 2000
    },
    "total_estimated_inr": 65500,
    "notes": "Budget sufficient for smooth BGMI gameplay at recommended settings with emulator."
  }
}
```

---

### 3️⃣ Validate PC for Game

Check if a PC build can run a specific game and at what performance level.

**Endpoint**: `POST /api/ai/validate-pc-for-game`

**Request**:
```json
{
  "game_name": "Cyberpunk 2077",
  "pc_specs": {
    "cpu_name": "Intel Core i7-13700K",
    "cpu_cores": 16,
    "gpu_name": "NVIDIA RTX 4070",
    "gpu_vram": 12,
    "ram_gb": 32,
    "storage_gb": 500
  }
}
```

**Response**:
```json
{
  "success": true,
  "game_name": "Cyberpunk 2077",
  "source": "openai",
  "compatibility": {
    "can_run": true,
    "performance_level": "Ultra 1440p",
    "expected_fps_1080p": "100-120 FPS",
    "expected_fps_1440p": "70-90 FPS",
    "bottleneck": "None",
    "upgrade_needed": false,
    "compatibility_score": 95,
    "notes": "Excellent build for Cyberpunk 2077. Can achieve ultra settings with ray tracing."
  }
}
```

---

## Example Usage - BGMI PC Build

### Step 1: Get BGMI Requirements
```bash
curl -X POST http://localhost:5000/api/ai/game-requirements \
  -H "Content-Type: application/json" \
  -d '{"game_name":"BGMI"}'
```

### Step 2: Get AI Recommendation for ₹80,000 Budget
```bash
curl -X POST http://localhost:5000/api/ai/game-build-recommendation \
  -H "Content-Type: application/json" \
  -d '{
    "game_name": "BGMI",
    "budget": 80000,
    "domain": "gaming"
  }'
```

### Step 3: Validate a PC for BGMI
```bash
curl -X POST http://localhost:5000/api/ai/validate-pc-for-game \
  -H "Content-Type: application/json" \
  -d '{
    "game_name": "BGMI",
    "pc_specs": {
      "cpu_name": "Intel Core i5-12400",
      "cpu_cores": 6,
      "gpu_name": "NVIDIA GTX 1650",
      "gpu_vram": 4,
      "ram_gb": 16,
      "storage_gb": 256
    }
  }'
```

---

## Supported Games

✅ **All Games Supported!**

Examples:
- 🎮 **AAA Games**: Cyberpunk 2077, Elden Ring, Baldur's Gate 3, Starfield
- 📱 **Mobile Games**: BGMI, PUBG Mobile, Fortnite, Call of Duty Mobile
- 🏎️ **Racing**: F1 24, Forza Motorsport
- ⚽ **Sports**: FC 25, NBA 2K25
- 🎬 **Video Editing Apps**: Adobe Premiere Pro, DaVinci Resolve
- 🎨 **3D Tools**: Blender, Maya, Cinema 4D
- Any game ever made!

---

## Response Codes

| Code | Meaning |
|------|---------|
| 200 | Success ✅ |
| 400 | Bad request (invalid game name or budget) |
| 500 | Server error (usually API key not set) |

---

## Error Handling

If you get this error:
```json
{
  "success": false,
  "error": "OpenAI API key not configured."
}
```

**Solution**: Set the `OPENAI_API_KEY` environment variable

```bash
# Windows PowerShell
$env:OPENAI_API_KEY="sk-your-key"

# Or run setup
python setup_openai.py
```

---

## Integration with Frontend

### 1. Update ai-game-input.html

```javascript
// When user selects a game, fetch requirements
async function selectGame(gameName) {
  const response = await fetch('/api/ai/game-requirements', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({game_name: gameName})
  });
  
  const data = await response.json();
  if (data.success) {
    console.log('Game requirements:', data.data);
    // Display requirements to user
    displayGameSpecs(data.data);
  }
}
```

### 2. Update build recommendations

```javascript
// Get AI recommendation
async function getAIBuild(gameName, budget, domain) {
  const response = await fetch('/api/ai/game-build-recommendation', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      game_name: gameName,
      budget: budget,
      domain: domain
    })
  });
  
  const data = await response.json();
  return data;
}
```

---

## Cost Considerations

- **GPT-3.5-turbo**: ~$0.001 per request (very cheap)
- **Average cost per game analysis**: $0.002-0.005
- 1000 queries = ~$2-5

---

## Troubleshooting

### Q: "Invalid API key" error?
**A**: Check your OpenAI API key is valid at https://platform.openai.com/api-keys

### Q: Slow responses?
**A**: First request is slower. Subsequent requests are faster. You can cache results.

### Q: Game info seems inaccurate?
**A**: OpenAI sometimes makes estimates. For critical specs, verify against official game requirements.

### Q: How do I use GPT-4 instead of 3.5?
**A**: Edit `openai_game_analyzer.py`:
```python
self.model = "gpt-4"  # More expensive but more accurate
```

---

## Next Steps

1. ✅ Run `python setup_openai.py`
2. ✅ Enter your OpenAI API key
3. ✅ Restart server with `python run.py`
4. ✅ Try API endpoints above
5. ✅ Integrate with frontend forms

---

## Support

For issues:
1. Check OpenAI API status: https://status.openai.com
2. Verify API key is set: `echo $OPENAI_API_KEY`
3. Check error logs in terminal

---

**🎉 Your PC builder now supports ANY game in the world!**
