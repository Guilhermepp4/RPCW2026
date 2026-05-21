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

def explore_mon(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    page = requests.get(url, headers=headers)
    page.encoding = 'utf-8'
    soup = BeautifulSoup(page.text, 'html.parser')

    res = {
        "Outros_Nomes": "",
        "Descricao": ""
    }

    content = soup.find('table', class_='table table-striped')
    if not content:
        return res
    
    td_label = content.find(lambda tag: tag.name == 'td' and "Outras Designações / Pesquisas" in tag.get_text())
    
    if td_label:
        td_conteudo = td_label.find_next_sibling('td')

        if td_conteudo:
            texto_completo = td_conteudo.get_text()
            subNames = texto_completo.replace("Ver Ficha em www.monumentos.gov.pt", "")
            res["Outros_Nomes"] = subNames.strip().strip('"').strip('(').strip(')').strip().strip('"')
    
    todos_tds = content.find_all('td')
    texto_mais_longo = ""
    
    for td in todos_tds:
        conteudo_td = td.get_text(separator="\n", strip=True)
        
        if "Ver Ficha em" in conteudo_td or "Descrição Geral" in conteudo_td or "Histórico" in conteudo_td or "Designações" in conteudo_td:
            continue
            
        if len(conteudo_td) > len(texto_mais_longo):
            texto_mais_longo = conteudo_td

    if len(texto_mais_longo) > 100:
        res["Descricao"] = texto_mais_longo.strip().strip('"').strip()

    return res

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
                    if cols[0].a:
                        next_url = cols[0].a["href"]
                        mon_info = explore_mon(next_url)
                    
                res["Concelhos"][concelho_name].append({
                    "ID": cols[0].get_text().strip(),
                    "Outros_Nomes": mon_info['Outros_Nomes'],
                    "Descrição": mon_info['Descricao']
                })
                print(f"Concelho: {concelho_name}, Monumento: {cols[1].get_text().strip()}")
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
f_out = open("monumentos.json", "w", encoding='utf-8')
json.dump(res, f_out, indent=4, ensure_ascii=False)

print("Ficheiro gerado com sucesso!")
print("Distritos:", len(res["Distritos"]))
print("Concelhos por distrito:")
for distrito, info in res["Distritos"].items():
    print(f"Distrito: {distrito}: {len(res['Distritos'][distrito]['Concelhos'])} concelhos")
