from flask import Flask, jsonify, render_template, request
from datetime import datetime
from mquery import execute_query, execute_update
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

def verificar_se_existe_na_ontologia(nome, tipo):
    query = f"""
    PREFIX : <http://www.semanticweb.org/guilhermepinho/ontologies/2026/3/monumentosPT/>
    ASK {{
        :{nome} a :{tipo} .
    }}
    """
    res = execute_query(query)
    return res.get('boolean', False)

@app.route('/inserir', methods=['GET', 'POST'])
def inserirMonumentoRoute():

    if request.method == 'GET':
        return render_template("addMonumento.html")
    
    id_monumento = request.form.get('id_monumento')
    id_existe = verificar_se_existe_na_ontologia(f"mon_{id_monumento}", "Monumento")
    if id_existe:
        return jsonify({'status': 'erro', 'mensagem': f"O ID '{id_monumento}' já existe na ontologia. Por favor, escolha um ID diferente."})
    
    nome = request.form.get('nome')
    subnomes = request.form.get('subnomes', 'n\a')
    ano = request.form.get('ano_fundacao', 'n\a')
    tipo = request.form.get('tipo_classe')
    tipologia = request.form.get('tipologia', 'n\a')
    id_concelho = request.form.get('concelho').strip().lower().replace(" ", "_")
    id_freguesia = request.form.get('freguesia').strip().lower().replace(" ", "_")
    latitude = request.form.get('latitude', 'n\a')
    longitude = request.form.get('longitude', 'n\a')
    imagem = request.form.get('imagem', 'http://www.sem-imagem.com')
    descricao = request.form.get('descricao', 'n\a')

    ilha_raw = request.form.get('ilha_nova')
    id_ilha = ilha_raw.strip().lower().replace(" ", "_") if ilha_raw else None

    distrito_raw = request.form.get('distrito_novo')
    id_distrito = distrito_raw.strip().lower().replace(" ", "_") if distrito_raw else None

    concelho_existe = verificar_se_existe_na_ontologia(f"conc_{id_concelho}", "Concelho")
    freguesia_existe = verificar_se_existe_na_ontologia(f"freg_{id_freguesia}", "Freguesia")
    criar_automatico = request.form.get('criar_automatico') == 'true'

    if (not concelho_existe or not freguesia_existe) and not criar_automatico:
        if not concelho_existe and not freguesia_existe:
            msg = f"O concelho '{id_concelho}' e a freguesia '{id_freguesia}' não existem. Indique o distrito para criarmos o concelho. A freguesia será criada e associada a ele."
            return jsonify({
                'status': 'aviso_locais', 
                'mensagem': msg, 
                'concelho_em_falta': True
            })

        elif concelho_existe and not freguesia_existe:
            msg = f"A freguesia '{id_freguesia}' não existe na ontologia. Deseja criá-la automaticamente e associá-la ao concelho '{id_concelho}'?"
            return jsonify({
                'status': 'aviso_locais', 
                'mensagem': msg, 
                'concelho_em_falta': False
            })

        elif not concelho_existe and freguesia_existe:
            msg = f"O concelho '{id_concelho}' não existe. Indique o distrito a que pertence para o podermos criar."
            return jsonify({
                'status': 'aviso_locais', 
                'mensagem': msg, 
                'concelho_em_falta': True
            })

    print(request.form.get('freguesia'))
    try:
        created = []

        if not concelho_existe:
            if id_ilha:
                pertence = f":pertence_Ilha :ilha_{id_ilha}"
            else:
                pertence = f":pertence_Distrito :dist_{id_distrito}"

            query_conc = f"""
            PREFIX : <http://www.semanticweb.org/guilhermepinho/ontologies/2026/3/monumentosPT/>
            INSERT DATA {{
                :conc_{id_concelho} a :Concelho ;
                    :nome "{request.form.get('concelho').strip()}" ;
                    {pertence} .
            }}
            """
            execute_update(query_conc)
            created.append(f"Concelho '{id_concelho}'")

        if not freguesia_existe:
            query_freg = f"""
            PREFIX : <http://www.semanticweb.org/guilhermepinho/ontologies/2026/3/monumentosPT/>
            INSERT DATA {{
                :freg_{id_freguesia} a :Freguesia ;
                    :nome "{request.form.get('freguesia').strip()}" ;
                    :pertence_concelho :conc_{id_concelho} .
            }}
            """
            execute_update(query_freg)
            created.append(f"Freguesia '{id_freguesia}'")

        triplos = [
        f""":mon_{id_monumento} a :{tipo} .
            :mon_{id_monumento} :nome "{nome}" .
            :mon_{id_monumento} :ficaEmConcelho :conc_{id_concelho} .
            :mon_{id_monumento} :ficaEmFreguesia :freg_{id_freguesia} ."""
        ]
        
        if ano:
            triplos.append(f':mon_{id_monumento} :Ano_Fundacao "{ano}" .')
        if tipologia:
            triplos.append(f':mon_{id_monumento} :temTipologia "{tipologia}" .')
        if subnomes:
            triplos.append(f':mon_{id_monumento} :temOutrosNomes "{subnomes}" .')
        if latitude:
            triplos.append(f':mon_{id_monumento} :temLatitude {latitude} .')
        if longitude:
            triplos.append(f':mon_{id_monumento} :temLongitude {longitude} .')
        if imagem:
            triplos.append(f':mon_{id_monumento} :temImagemURL <{imagem}> .')
        if descricao:
            triplos.append(f':mon_{id_monumento} :temDescricao "{descricao}" .')
        
        corpo_query = "\n        ".join(triplos)
        query = f"""
        PREFIX : <http://www.semanticweb.org/guilhermepinho/ontologies/2026/3/monumentosPT/>
        INSERT DATA {{
            {corpo_query}
        }}
        """

        execute_update(query)
        created.append(f"Monumento '{id_monumento}'")

        return jsonify({'status': 'sucesso', 'mensagem': f"Sucesso! Os seguintes elementos foram criados: {', '.join(created)}"})

    except Exception as e:
        return jsonify({'status': 'erro', 'mensagem': f'Erro ao executar SPARQL: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True)