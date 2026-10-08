from server.services.openai_game_analyzer import MOCK_GAMES_DATABASE

print('Total games in database:', len(MOCK_GAMES_DATABASE))
print('\nFirst 15 games:')
for i, (key, game) in enumerate(list(MOCK_GAMES_DATABASE.items())[:15]):
    print(f"{i+1}. {game.get('game_name')} - {game.get('source')}")
