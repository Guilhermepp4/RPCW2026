import requests
import re
from bs4 import BeautifulSoup
import json

url_base = "https://pt.wikipedia.org/wiki/Lista_de_patrim%C3%B3nio_edificado_n"
res = {
    "Arquipelago": {}
}

Arquipelago = ["os_Açores", "a_Madeira"]

def extrairInf(page_response, açores):
    page_response.encoding = 'utf-8'
    soup = BeautifulSoup(page_response.text, 'html.parser')

    res = {
        "Ilha": {}
    }

    content = soup.find('div', class_='mw-parser-output')
    sections = content.find_all("section", {"aria-labelledby": True}, recursive=False)

    if açores:
        sections = sections[1:-2]

    for sec in sections:
        ilha = sec.find('h2')
        print("Encontrada ilha:", ilha.get_text(strip=True))
        ilha_name = re.sub(r"Ilha\s*d[aeo]\s*", "", ilha.get_text(strip=True)).strip()
        #print(f"Processando ilha: {ilha_name}")
        
        res["Ilha"][ilha_name] = {
            "Concelhos": {}
        }

        sections2 = sec.find_all("section", {"aria-labelledby": True}, recursive=False)

        for sec2 in sections2:
            concelho_name = re.sub(r"Concelho\s*d[aeo]\s*", "", sec2.find('h3').get_text(strip=True)).strip()
            print(f"Processando concelho: {concelho_name}")
            res["Ilha"][ilha_name]["Concelhos"][concelho_name] = []

            tabela = sec2.find('table')
            if not tabela:
                continue
            
            if açores:
                i = 2
            else:
                i = 1

            rows = tabela.find_all('tr')[i:]

            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 7:
                    id = cols[0].get_text(strip=True).strip() or ""
                    designacao = cols[1].get_text(strip=True).strip()
                    categoria = cols[2].get_text(strip=True).strip()
                    tipologia = cols[3].get_text(strip=True).strip()
                    freguesia = cols[4].get_text(strip=True).strip()
                    grau = cols[5].get_text(strip=True).strip()
                    ano = cols[6].get_text(strip=True).strip()

                    coordenadas = None
                    imagem = None
                    if len(cols) > 7:
                        coordenadas = cols[7].get_text().strip()
                        imagem = cols[8].find('img')['src'] if len(cols) > 8 and cols[8].find('img') else None
                
                res["Ilha"][ilha_name]["Concelhos"][concelho_name].append({
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

for arq in Arquipelago:
    try:
        fullink = url_base + arq
        page = requests.get(fullink, headers=headers)
        arquipelago = arq.split("_")[-1]
        print(f"Processando arquipelago: {arquipelago}")
        if arq == "os_Açores":
            açores = True
        else:
            açores = False
        res["Arquipelago"][arquipelago] = extrairInf(page, açores)

    except Exception as e:
        print(f"Erro arquipelago {arquipelago}: {e}")


res["Arquipelago"] = dict(
    sorted(res["Arquipelago"].items(), key=lambda x: x[0])
)
f_out = open("datasets/monumentosARQ.json", "w", encoding='utf-8')
json.dump(res, f_out, indent=4, ensure_ascii=False)

print("Ficheiro gerado com sucesso!")
print("Arquipelagos:", len(res["Arquipelago"]))
print("Ilhas por arquipelago:")
for arquipelago, info in res["Arquipelago"].items():
    print(f"Arquipelago: {arquipelago}: {len(res['Arquipelago'][arquipelago]['Ilha'])} ilhas")
