import pandas as pd

df = pd.read_csv("ficheiro.csv", sep=";")

df = df.drop(columns=[
    "nuts1_cod",
    "nuts2_cod",
    "nuts3_cod"
])

df.to_csv("ficheiro_limpo.csv", index=False)