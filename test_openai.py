#!/usr/bin/env python3
"""
Quick test script for OpenAI Game Analyzer.
Run this to verify your OpenAI integration is working.
"""

import os
import json
import sys

def test_openai_setup():
    """Test if OpenAI is properly configured."""
    print("\n" + "="*60)
    print("🧪 Testing OpenAI Game Analyzer Setup")
    print("="*60 + "\n")
    
    # Check API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment")
        print("\n📝 Setup instructions:")
        print("   1. Run: python setup_openai.py")
        print("   2. Enter your OpenAI API key")
        print("   3. Restart the server: python run.py")
        return False
    
    print(f"✅ OpenAI API key found: {api_key[:10]}...")
    
    # Try to import and initialize
    try:
        from server.services.openai_game_analyzer import OpenAIGameAnalyzer
        print("✅ OpenAI Game Analyzer imported successfully")
        
        analyzer = OpenAIGameAnalyzer()
        print("✅ Analyzer initialized successfully")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Run test queries
    test_games = ["BGMI", "Cyberpunk 2077", "Minecraft"]
    
    print("\n🎮 Testing game requirement extraction:\n")
    
    for game in test_games:
        try:
            print(f"  Analyzing: {game}...", end=" ", flush=True)
            result = analyzer.extract_game_requirements(game)
            
            if result['success']:
                data = result['data']
                print(f"✅")
                print(f"     - Platforms: {', '.join(data.get('platforms', []))}")
                print(f"     - Min CPU Cores: {data.get('minimum', {}).get('cpu_cores', 'N/A')}")
                print(f"     - Min GPU VRAM: {data.get('minimum', {}).get('gpu_vram', 'N/A')}GB")
                print(f"     - Min RAM: {data.get('minimum', {}).get('ram_gb', 'N/A')}GB")
            else:
                print(f"⚠️  {result.get('error', 'Unknown error')}")
        
        except Exception as e:
            print(f"❌ Error: {str(e)[:50]}")
    
    print("\n" + "="*60)
    print("✨ Setup Complete!")
    print("="*60)
    print("\n📖 API Documentation: See OPENAI_SETUP.md")
    print("\n🚀 Available Endpoints:")
    print("   POST /api/ai/game-requirements")
    print("   POST /api/ai/game-build-recommendation")
    print("   POST /api/ai/validate-pc-for-game")
    print("\n💡 Example Request:")
    print("   curl -X POST http://localhost:5000/api/ai/game-requirements \\")
    print('     -H "Content-Type: application/json" \\')
    print('     -d \'{"game_name":"BGMI"}\'')
    
    return True

if __name__ == '__main__':
    success = test_openai_setup()
    sys.exit(0 if success else 1)
