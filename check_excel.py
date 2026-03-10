import pandas as pd

df = pd.read_excel('infoenfermedades.xlsx')
print('Patologías en Excel:')
for i, p in enumerate(df['Patología'].tolist(), 1):
    print(f'{i}. {p}')
