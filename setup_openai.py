"""
Setup script for OpenAI API integration.
Run this once to configure your OpenAI API key.
"""

import os
import sys

def setup_openai_key():
    """Set up OpenAI API key in environment."""
    print("\n" + "="*60)
    print("🚀 OpenAI API Configuration Setup")
    print("="*60)
    
    api_key = input("\n📝 Enter your OpenAI API Key: ").strip()
    
    if not api_key:
        print("❌ No API key provided. Setup cancelled.")
        return False
    
    if not api_key.startswith('sk-'):
        print("⚠️  Warning: API key should start with 'sk-'")
        confirm = input("Continue anyway? (y/n): ").strip().lower()
        if confirm != 'y':
            return False
    
    # Create .env file
    env_content = f"OPENAI_API_KEY={api_key}\n"
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ API key saved to .env file")
    
    # Also add to environment for current session
    os.environ['OPENAI_API_KEY'] = api_key
    
    # Verify by testing import
    try:
        from server.services.openai_game_analyzer import OpenAIGameAnalyzer
        analyzer = OpenAIGameAnalyzer(api_key)
        print("✅ OpenAI analyzer initialized successfully")
        print("\n✨ Setup complete! You can now:")
        print("   - Search for any game (BGMI, Cyberpunk 2077, etc.)")
        print("   - Get hardware requirements automatically")
        print("   - Receive AI-powered build recommendations")
        print("\n🎮 Try it: POST /api/ai/game-requirements")
        print('        {"game_name": "BGMI"}')
        return True
    except Exception as e:
        print(f"❌ Error initializing analyzer: {e}")
        return False

if __name__ == '__main__':
    if setup_openai_key():
        sys.exit(0)
    else:
        sys.exit(1)
