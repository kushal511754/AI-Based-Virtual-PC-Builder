"""Load environment variables and test OpenAI."""
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Load .env file
from dotenv import load_dotenv
env_path = project_root / '.env'
load_dotenv(dotenv_path=env_path)

# Verify API key loaded
api_key = os.getenv('OPENAI_API_KEY')
if api_key:
    print(f"✅ API Key loaded: {api_key[:20]}...")
else:
    print("❌ API Key not found")

# Now test
if __name__ == '__main__':
    from server.services.openai_game_analyzer import OpenAIGameAnalyzer
    
    try:
        analyzer = OpenAIGameAnalyzer()
        print("✅ OpenAI Analyzer initialized successfully")
        
        # Test with BGMI
        print("\n🎮 Testing BGMI requirements extraction...")
        result = analyzer.extract_game_requirements("BGMI")
        
        if result['success']:
            print("✅ BGMI analysis successful!")
            data = result['data']
            print(f"   Game: {data.get('game_name')}")
            print(f"   Platforms: {', '.join(data.get('platforms', []))}")
            print(f"   Min CPU Cores: {data.get('minimum', {}).get('cpu_cores')}")
            print(f"   Min GPU VRAM: {data.get('minimum', {}).get('gpu_vram')}GB")
            print(f"   Min RAM: {data.get('minimum', {}).get('ram_gb')}GB")
        else:
            print(f"❌ Error: {result.get('error')}")
    
    except Exception as e:
        print(f"❌ Error: {e}")
