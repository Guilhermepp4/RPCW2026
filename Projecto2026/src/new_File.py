import requests
import re
from bs4 import BeautifulSoup
import json

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

res = explore_mon("https://imovel.patrimoniocultural.gov.pt/detalhes.php?code=70350")

with open("teste.json", "w", encoding='utf-8') as f_out:
    json.dump(res, f_out, indent=4, ensure_ascii=False)