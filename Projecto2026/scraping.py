import requests
import re
from bs4 import BeautifulSoup
import json

url_base = "https://www.dges.gov.pt/guias/inddist.asp?dist="
res = {
    "Universidades": {},
    "Escolas": {}
}

def parse_regime(regime):
    tipo = None
    natureza = None

    if "Militar e Policial" in regime:
        tipo = "Militar e Policial"
    elif "Universitário" in regime:
        tipo = "Universidade"
    elif "Politécnico" in regime:
        tipo = "Politécnico"

    if "Público" in regime:
        natureza = "Público"
    elif "Privado" in regime:
        natureza = "Privado"

    return tipo, natureza

def get_regiao(distrito):
    norte = ["Porto", "Braga", "Viana do Castelo", "Bragança", "Vila Real"]
    centro = ["Coimbra", "Aveiro", "Leiria", "Guarda", "Castelo Branco", "Viseu"]
    lisboa = ["Lisboa", "Setúbal", "Santarém"]
    alentejo = ["Évora", "Beja", "Portalegre"]
    algarve = ["Faro"]
    ilhas = ["Açores", "Madeira"]

    if distrito in norte:
        return "Norte"
    if distrito in centro:
        return "Centro"
    if distrito in lisboa:
        return "Lisboa"
    if distrito in alentejo:
        return "Alentejo"
    if distrito in algarve:
        return "Algarve"
    if distrito in ilhas:
        return "Ilhas"
    return "Desconhecido"

def clean(text):
    return re.sub(r'\s+', ' ', text).strip()

def extrairInf(page_response):
    page_response.encoding = 'iso-8859-1'
    soup = BeautifulSoup(page_response.text, 'html.parser')

    local = soup.find('p', class_='box10')
    distrito = clean(local.get_text(" ")) if local else "Desconhecido"
    regiao = get_regiao(distrito)

    current_regime = None

    # 🔥 PERCORRER HTML NA ORDEM (FIX PRINCIPAL)
    for tag in soup.find_all('div'):

        classes = tag.get('class', [])

        # atualizar regime
        if 'lin-regime' in classes:
            current_regime = clean(tag.get_text())
            continue

        # processar instituição
        if 'lin-est' in classes:

            codigo = None
            nomeUniversidade = clean(tag.get_text())

            match = re.match(r'(\d+)(.*)', nomeUniversidade)
            if match:
                codigo = match.group(1)
                nomeUniversidade = match.group(2).strip()

            partes = nomeUniversidade.split(" - ")

            if len(partes) == 2:
                estabelecimento = partes[0].strip()
                nome = partes[1].strip()
            else:
                estabelecimento = nomeUniversidade
                nome = nomeUniversidade

            # universidades (sem duplicar)
            if estabelecimento not in res['Universidades']:
                res['Universidades'][estabelecimento] = {
                    "id": codigo,
                    "Nome": estabelecimento
                }

            # escolas (evita overwrite usando chave única)
            chave = f"{estabelecimento}::{nome}"

            tipo, natureza = parse_regime(current_regime)
            res['Escolas'][chave] = {
                "Nome": nome,
                "Instituicao": estabelecimento,
                "Distrito": distrito,
                "Região": regiao,
                "Tipo": tipo,
                "Natureza": natureza
            }


dist_ids = [str(i).zfill(2) for i in range(1, 23)]

for dist in dist_ids:
    try:
        fullink = url_base + dist
        page = requests.get(fullink,)
        extrairInf(page)

    except Exception as e:
        print(f"Erro distrito {dist}: {e}")

res["Escolas"] = sorted(res["Escolas"].values(), key=lambda x: x["Distrito"])
f_out = open("datasets/universidades.json", "w", encoding='utf-8')
json.dump(res, f_out, indent=4, ensure_ascii=False)

print("Ficheiro gerado com sucesso!")
print("Universidades:", len(res["Universidades"]))
print("Escolas:", len(res["Escolas"]))