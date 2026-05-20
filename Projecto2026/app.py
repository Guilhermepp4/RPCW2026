from flask import Flask, render_template, request
from datetime import datetime
from mquery import execute_query

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
        
        ?concelho :pertence_Distrito ?distrito ;
                  :nome ?nconcelho .
        ?distrito :pertenceA_Regiao ?regiao ;
                  :nome ?ndistrito .
        ?regiao a :Região ;
                :nome ?nregiao .
        
        BIND(STRAFTER(str(?tipoIndividuo), "monumentosPT/") as ?normaType)
        BIND(STRAFTER(str(?m), "monumentosPT/") as ?id)

        # Filtros
        FILTER(?normaType != "Monumento" && ?normaType != "NamedIndividual" && ?normaType != "")
        {filtro_distrito}
        {filtro_tipo}
    }}
    ORDER BY ?ndistrito ?nconcelho ?nome
    """
    
    res = execute_query(query)
    
    lista_monumentos = []
    if res and "results" in res:
        infos = res['results']['bindings']
        for info in infos:
            tipo = info.get('normaType', {}).get('value', 'Desconhecido')
            lat = info.get('lat', {}).get('value')
            lng = info.get('long', {}).get('value')
            if tipo == 'Desconhecido':
                continue

            lista_monumentos.append({
                "id": info.get('id', {}).get('value', ''),
                "name": info.get('nome', {}).get('value', 'S/ Nome'),
                "tipo": tipo,
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
    ilhas_aberto = any(d in distritos for d in ["Açores", "Madeira"])

    return render_template("start.html", monumentos=lista_monumentos, distritos_selecionadas=distritos, tipos_selecionados=type, norte_aberto=norte_aberto, centro_aberto=centro_aberto, lisboa_aberto=lisboa_aberto, alentejo_aberto=alentejo_aberto, algarve_aberto=algarve_aberto, ilhas_aberto=ilhas_aberto)

@app.route('/monumento/<id_monumento>')
def monumentoRoute(id_monumento):
    return render_template("monumento.html", id=id_monumento)

if __name__ == '__main__':
    app.run(debug=True)