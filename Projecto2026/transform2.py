import pandas as pd
import re

df = pd.read_excel('freguesias-de-portugal-websites-e-historico-de-versoes-no-arquivopt.xlsx', skiprows=1)

# Suprepondo que a tua coluna se chama 'Localizacao'
# Vamos extrair apenas o que está dentro dos parênteses
df['Concelho'] = df['Freguesia e concelho'].str.extract(r'\((.*?)\)')

# Se quiseres remover a coluna antiga e ficar só com a nova:
df = df.drop(columns=['Freguesia e concelho'])

# 2. Guardar em CSV
df.to_csv('freguesias.csv', index=False, encoding='utf-8')