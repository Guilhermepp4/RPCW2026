from flask import Flask, render_template, request
from datetime import datetime
from mquery import execute_query
import re

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("start.html", monumentos=[])

# Rota de Pesquisa (Ligada ao action="/pesquisar" do teu formulário)
@app.route('/pesquisar', methods=['POST'])
def pesquisar():
    distritos = request.form.getlist('distrito')
    type = request.form.getlist('tipo_local')
    
    for t in type:
        t = t.strip()
    if distritos:
        formatados = ", ".join([f'"{d}"' for d in distritos])
        filtro_distrito = f"FILTER (?ndistrito IN ({formatados}))"
    else:
        filtro_distrito = ""

    if type:
        form_types = ", ".join([f'"{t}"' for t in type])
        filtro_tipo = f"FILTER (?normaType IN ({form_types}))"
    else:
        filtro_tipo = ""

    query = f"""
    PREFIX : <http://www.semanticweb.org/guilhermepinho/ontologies/2026/3/monumentosPT/>
    SELECT DISTINCT ?id ?nome ?normaType ?ndistrito ?nconcelho ?nregiao ?lat ?long WHERE {{
    
    ?m a ?tipoIndividuo ;
       :nome ?nome ;
       :ficaEmConcelho ?concelho .
       
    OPTIONAL {{ ?m :temLatitude ?lat . }}
    OPTIONAL {{ ?m :temLongitude ?long . }}
        
        ?concelho :nome ?nconcelho .
        {{
         	?concelho :pertence_Distrito ?distrito .
            ?distrito :nome ?ndistrito ;
            		:pertenceA_Regiao/:nome ?nregiao .
        }} UNION {{
            ?concelho :pertence_Ilha ?ilha .
            ?ilha :nome ?ndistrito ;
            	:pertenceArquipelago/:nome ?nregiao .
        }}
        
        BIND(STRAFTER(str(?tipoIndividuo), "monumentosPT/") as ?normaType)
        BIND(STRAFTER(str(?m), "monumentosPT/") as ?id)
		
        FILTER(?normaType != "Monumento" && ?normaType != "NamedIndividual" && ?normaType != "")
    	
        {filtro_distrito}
        {filtro_tipo}
    }}
    ORDER BY ?ndistrito ?nconcelho ?nome
    """
    
    res = execute_query(query)
    # Três Grutas ou Grutas de São Bartolomeu
    lista_monumentos = []
    if res and "results" in res:
        infos = res['results']['bindings']
        for info in infos:
            tipo = info.get('normaType', {}).get('value', 'Desconhecido')
            nome = info.get('nome', {}).get('value', '')
            nome_norm = re.split(r"/|\bou\b", nome)[0]
            lat = info.get('lat', {}).get('value')
            lng = info.get('long', {}).get('value')
            if tipo == 'Desconhecido' or nome == '':
                continue

            TRADUCAO_TIPOS = {
                "ArquiteturaMista": "Arquitetura Mista",
                "EdificioReligioso": "Edifício Religioso",
                "EstruturaMilitar": "Estrutura Militar",
                "MonumentoCivil": "Monumento Civil",
                "SitioArqueologico": "Sítio Arqueológico",
                "Outros": "Outros"
            }

            lista_monumentos.append({
                "id": info.get('id', {}).get('value', ''),
                "name": nome_norm,
                "tipo": TRADUCAO_TIPOS.get(tipo, tipo),
                "distrito": info.get('ndistrito', {}).get('value', 'S/ Distrito'),
                "concelho": info.get('nconcelho', {}).get('value', 'S/ Concelho'),
                "regiao": info.get('nregiao', {}).get('value', 'S/ Região')
            })
            try:
                lista_monumentos[-1]["lat"] = float(lat)
                lista_monumentos[-1]["long"] = float(lng)
            except:
                pass
    
    norte_aberto = any(d in distritos for d in ["Braga", "Bragança", "Porto", "Viana do Castelo", "Vila Real"])
    centro_aberto = any(d in distritos for d in ["Aveiro", "Castelo Branco", "Coimbra", "Guarda", "Leiria", "Viseu"])
    lisboa_aberto = any(d in distritos for d in ["Lisboa", "Santarém", "Setúbal"])
    alentejo_aberto = any(d in distritos for d in ["Beja", "Évora", "Portalegre"])
    algarve_aberto = "Faro" in distritos
    ilhas_aberto = any(d in distritos for d in ["Corvo", "Flores", "Pico", "Graciosa", "Santa Maria", "São Jorge", "São Miguel", "Terceira", "Madeira", "Porto Santo"])

    return render_template("start.html", monumentos=lista_monumentos, distritos_selecionados=distritos, tipos_selecionados=type, norte_aberto=norte_aberto, centro_aberto=centro_aberto, lisboa_aberto=lisboa_aberto, alentejo_aberto=alentejo_aberto, algarve_aberto=algarve_aberto, ilhas_aberto=ilhas_aberto)

@app.route('/monumento/<id_monumento>')
def monumentoRoute(id_monumento):
    q = f"""
    PREFIX : <http://www.semanticweb.org/guilhermepinho/ontologies/2026/3/monumentosPT/>
    SELECT Distinct ?NameMon ?subNomes ?normaType ?Year ?tipo ?lat ?long ?img ?nregiao ?ndistrito ?NameConc ?NameFreg ?descricao WHERE {{
        :{id_monumento} a ?tipoMonumento ;
            :nome ?NameMon ;
            :ficaEmConcelho ?Conc ;
            :ficaEmFreguesia/:nome ?NameFreg .
        
        ?Conc a :Concelho ;
            :nome ?NameConc .
        
        {{
        ?Conc :pertence_Distrito ?distrito .
        ?distrito :nome ?ndistrito ;
                    :pertenceA_Regiao/:nome ?nregiao .
        }} UNION {{
        ?Conc :pertence_Ilha ?ilha .
        ?ilha :nome ?ndistrito ;
                :pertenceArquipelago/:nome ?nregiao .
        }}
        
        OPTIONAL {{ :{id_monumento} :temTipologia ?tipo . }}
        OPTIONAL {{ :{id_monumento} :temLatitude ?lat . }}
        OPTIONAL {{ :{id_monumento} :temLongitude ?long . }}
        OPTIONAL {{ :{id_monumento} :temImagemURL ?img . }}
        OPTIONAL {{ :{id_monumento} :Ano_Fundacao ?Year . }}
        OPTIONAL {{ :{id_monumento} :temOutrosNomes ?subNomes . }}
        OPTIONAL {{ :{id_monumento} :temDescricao ?descricao . }}

        BIND(STRAFTER(str(?tipoMonumento), "monumentosPT/") as ?normaType)
        FILTER(?normaType != "Monumento" && ?normaType != "NamedIndividual" && ?normaType != "")

    }}
    """

    res = execute_query(q)
    
    monumento = []
    if res and "results" in res:
        infos = res['results']['bindings']
        for info in infos:
            tipo = info.get('normaType', {}).get('value', 'Desconhecido')
            nome = info.get('NameMon', {}).get('value', '')
            nome_norm = re.split(r"/|\bou\b", nome)[0]
            lat = info.get('lat', {}).get('value')
            lng = info.get('long', {}).get('value')
            if tipo == 'Desconhecido' or nome == '':
                continue

            TRADUCAO_TIPOS = {
                "ArquiteturaMista": "Arquitetura Mista",
                "EdificioReligioso": "Edifício Religioso",
                "EstruturaMilitar": "Estrutura Militar",
                "MonumentoCivil": "Monumento Civil",
                "SitioArqueologico": "Sítio Arqueológico",
                "Outros": "Outros"
            }

            monumento.append({
                "nome": nome_norm,
                "tipo": TRADUCAO_TIPOS.get(tipo, tipo),
                "nregiao": info.get('nregiao', {}).get('value', 'S/ Região'),
                "ndistrito": info.get('ndistrito', {}).get('value', 'S/ Distrito'),
                "nconcelho": info.get('NameConc', {}).get('value', 'S/ Concelho'),
                "freguesia": info.get('NameFreg', {}).get('value', 'S/ Freguesia'),
            })
            if info.get('subNomes', {}).get('value'):
                monumento[-1].update({
                    "subNomes": info.get('subNomes', {}).get('value', ''),
                })
            if info.get('descricao', {}).get('value'):
                monumento[-1].update({
                    "descricao": info.get('descricao', {}).get('value', 'Sem descrição disponível.')
                })
            if info.get('tipo', {}).get('value'):
                monumento[-1].update({
                    "tipologia": info.get('tipo', {}).get('value', 'Desconhecido')
                })
            if info.get('Year', {}).get('value'):
                monumento[-1].update({
                    "ano": info.get('Year', {}).get('value', 'Desconecido')
                })
            if info.get('img', {}).get('value'):
                monumento[-1].update({
                    "imagem": info.get('img', {}).get('value', '')
                })
            try:
                monumento[-1]["lat"] = float(lat)
                monumento[-1]["long"] = float(lng)
            except:
                pass
            
    
    return render_template("monumento.html", monumento=monumento[-1])

@app.route('/inserir', methods=['GET', 'POST'])
def inserirMonumentoRoute():
    return render_template("addMonumento.html")

if __name__ == '__main__':
    app.run(debug=True)