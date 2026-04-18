import requests
import pandas as pd

url = "https://query.wikidata.org/sparql"

query = """
SELECT ?personLabel ?birthDate ?placeLabel ?occupationLabel WHERE {
  ?person wdt:P31 wd:Q5;
          wdt:P569 ?birthDate;
          wdt:P19 ?place;
          wdt:P106 ?occupation;
          wdt:P27 wd:Q45.

  SERVICE wikibase:label { bd:serviceParam wikibase:language "pt,en". }
}
LIMIT 1000
"""

headers = {
    "User-Agent": "Mozilla/5.0"
}

r = requests.get(url, params={"query": query, "format": "json"}, headers=headers)
data = r.json()

rows = []

for item in data["results"]["bindings"]:
    rows.append({
        "Nome": item["personLabel"]["value"],
        "DataNascimento": item.get("birthDate", {}).get("value", ""),
        "Distrito": "Desconhecido",
        "Concelho": item.get("placeLabel", {}).get("value", ""),
        "Freguesia": "Desconhecido",
        "Categoria": item.get("occupationLabel", {}).get("value", "")
    })

df = pd.DataFrame(rows)
df.to_csv("figuras_portuguesas.csv", index=False, encoding="utf-8")
print("CSV gerado com sucesso:", len(df))