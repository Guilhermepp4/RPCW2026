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
    SELECT DISTINCT ?nome ?normaType ?ndistrito ?nconcelho ?nregiao ?lat ?long WHERE {{
    
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

    return render_template("start.html", monumentos=lista_monumentos)

if __name__ == '__main__':
    app.run(debug=True)