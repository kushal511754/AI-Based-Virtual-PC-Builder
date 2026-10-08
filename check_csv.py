import pandas as pd

df = pd.read_csv('games.csv', encoding='utf-8', on_bad_lines='skip')
print('Columns:', df.columns.tolist())
print('\nFirst row data:')
for col in df.columns[:10]:
    print(f"{col}: {df.iloc[0][col]}")

