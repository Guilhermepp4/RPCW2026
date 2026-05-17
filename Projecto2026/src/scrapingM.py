import requests
import re
from bs4 import BeautifulSoup
import json

url_base = "https://pt.wikipedia.org/wiki/Lista_de_patrim%C3%B3nio_edificado_no_distrito_"
res = {
    "Distritos": {}
}

distritos = ["do_Porto#Porto", "de_Braga#Braga", "de_Viana_do_Castelo#Viana_do_Castelo",
              "de_Bragança#Bragança", "de_Vila_Real#Vila_Real",
              "de_Coimbra#Coimbra", "de_Aveiro#Aveiro", "de_Leiria#Leiria",
              "da_Guarda#Guarda", "de_Castelo_Branco#Castelo_Branco", "de_Viseu#Viseu",
              "de_Lisboa#Lisboa", "de_Setúbal#Setúbal", "de_Santarém#Santarém", 
              "de_Évora#Évora", "de_Beja#Beja", "de_Portalegre#Portalegre",
              "de_Faro#Faro"]

def extrairInf(page_response):
    page_response.encoding = 'utf-8'
    soup = BeautifulSoup(page_response.text, 'html.parser')

    res = {
        "Concelhos": {}
    }

    content = soup.find('div', class_='mw-parser-output')
    sections = content.find_all("section", {"aria-labelledby": True})
    for sec in sections:
        concelho_name = sec.find('h2').get_text().replace("Concelho de ", "").strip()
        res["Concelhos"][concelho_name] = []
        tabela = sec.find('table')
        if tabela:
            rows = tabela.find_all('tr')[1:]

            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 7:
                    id = cols[0].get_text().strip()
                    designacao = cols[1].get_text().strip()
                    categoria = cols[2].get_text().strip()
                    tipologia = cols[3].get_text().strip()
                    freguesia = cols[4].get_text().strip()
                    grau = cols[5].get_text().strip()
                    ano = cols[6].get_text().strip()
                    coordenadas = None
                    imagem = None
                    if len(cols) > 7:
                        coordenadas = cols[7].get_text().strip()
                        imagem = cols[8].find('img')['src'] if len(cols) > 8 and cols[8].find('img') else None
                res["Concelhos"][concelho_name].append({
                    "ID": id,
                    "Designação": designacao,
                    "Categoria": categoria,
                    "Tipologia": tipologia,
                    "Freguesia": freguesia,
                    "Grau": grau,
                    "Ano": ano,
                    "Coordenadas": coordenadas,
                    "Imagem": imagem
                })
    return res


headers = {
    "User-Agent": "Mozilla/5.0"
}

for dist in distritos:
    try:
        fullink = url_base + dist
        page = requests.get(fullink, headers=headers)
        distrito = dist.split("#")[1]
        res["Distritos"][distrito] = extrairInf(page)

    except Exception as e:
        print(f"Erro distrito {dist}: {e}")

res["Distritos"] = dict(
    sorted(res["Distritos"].items(), key=lambda x: x[0])
)
f_out = open("datasets/monumentos.json", "w", encoding='utf-8')
json.dump(res, f_out, indent=4, ensure_ascii=False)

print("Ficheiro gerado com sucesso!")
print("Distritos:", len(res["Distritos"]))
print("Concelhos por distrito:")
for distrito, info in res["Distritos"].items():
    print(f"Distrito: {distrito}: {len(res['Distritos'][distrito]['Concelhos'])} concelhos")
