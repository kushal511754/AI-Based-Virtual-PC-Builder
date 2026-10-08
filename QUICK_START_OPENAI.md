# ⚡ Quick Start - OpenAI Integration

## 3-Step Setup (5 minutes)

### Step 1: Get Your OpenAI API Key
1. Go to: https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy the key (starts with `sk-`)

### Step 2: Configure Your API Key
Choose ONE method:

**Method A: Interactive (Recommended)**
```bash
python setup_openai.py
# Paste your API key when prompted
```

**Method B: Manual - Edit `.env` file**
```
Open .env in this directory
Replace: OPENAI_API_KEY=sk-your-key-here
With your actual key
```

### Step 3: Restart & Test
```bash
# Kill current server (Ctrl+C if running)
# Restart
python run.py

# In another terminal, test:
python test_openai.py
```

---

## Try It Now! 🎮

### Test BGMI Support:
```bash
curl -X POST http://localhost:5000/api/ai/game-requirements \
  -H "Content-Type: application/json" \
  -d '{"game_name":"BGMI"}'
```

### Get Build for BGMI + ₹80,000:
```bash
curl -X POST http://localhost:5000/api/ai/game-build-recommendation \
  -H "Content-Type: application/json" \
  -d '{"game_name":"BGMI","budget":80000,"domain":"gaming"}'
```

---

## What You Get ✨

With OpenAI integration, you can now:

✅ **Search ANY game** - BGMI, Cyberpunk, Fortnite, anything
✅ **Get hardware requirements** - Automatic from AI
✅ **Generate builds** - With ₹ INR pricing from PCBuildAgent
✅ **Validate PCs** - Check if a PC can run any game
✅ **All games** - Mobile, PC, console games supported

---

## File Changes Made

**New Files:**
- `server/services/openai_game_analyzer.py` - AI game analyzer
- `setup_openai.py` - Setup script
- `test_openai.py` - Test script
- `OPENAI_SETUP.md` - Full documentation
- `OPENAI_IMPLEMENTATION.md` - Implementation details

**Modified Files:**
- `server/routes/ai_build.py` - 3 new endpoints
- `requirements.txt` - Added openai package
- `.env` - For your API key

---

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/ai/game-requirements` | POST | Get any game's specs |
| `/api/ai/game-build-recommendation` | POST | Get build + budget |
| `/api/ai/validate-pc-for-game` | POST | Validate PC for game |

---

## Support

- 📖 Full docs: See `OPENAI_SETUP.md`
- 🧪 Test: Run `python test_openai.py`
- ❓ Issues: Check `.env` file and API key

---

**Now your PC builder works with BGMI and ANY game! 🚀**
