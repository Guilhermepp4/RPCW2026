from flask import Flask, render_template
from datetime import datetime
from mquery import execute_query

app = Flask(__name__)

data_hora_local = datetime.now()
data_iso = data_hora_local.strftime('"%Y-%m-%dT%H:%M:%S')

@app.route('/')
@app.route('/livros')
def index():
    q= """
    PREFIX : <http://example.org/biblioteca-temporal#>
    SELECT ?LivroId ?titulo ?tipoId ?nomeAutor ?pais WHERE {  
        ?livro a ?tipoLivro .
        filter(?tipoLivro in (:LivroHistorico, :LivroFiccional, :LivroParadoxal))
        OPTIONAL{ ?livro :titulo ?titulo . }
        ?livro :escritoPor/:nome ?nomeAutor .
        ?livro :escritoPor/:paisOrigem ?pais .
        BIND(STRAFTER(STR(?livro), "#") AS ?LivroId)
        BIND(STRAFTER(STR(?tipoLivro), "#") AS ?tipoId)
    }  order by ?titulo    
    """
    res = execute_query(q)
    livros = []

    for livro in res['results']['bindings']:
        l = { "id": livro['LivroId']['value'],
                        "tipo": livro['tipoId']['value'],
                        "autor": livro['nomeAutor']['value'],
                        "pais": livro['pais']['value']
            }
        if "titulo" in livro:
            l["titulo"] = livro['titulo']['value']

        livros.append(l)
        
    return render_template("lista.html", livros = livros)


@app.route('/livro/<id_livro>')
def livroRoute(id_livro):
    q= f"""
    PREFIX : <http://example.org/biblioteca-temporal#>
    SELECT ?titulo ?livroTipo ?nomeAutor ?paisOri ?Linha ?LinhaTipo ?Evento ?nomeEvento ?eventoDesc WHERE {{
        :{id_livro} a ?tipoLivro ;
            :escritoPor/:nome ?nomeAutor ;
            :escritoPor/:paisOrigem ?paisOri ;
            :existeEm ?linha .
            ?linha a ?tipoLinha .
        FILTER(?tipoLivro IN (:LivroParadoxal, :LivroHistorico, :LivroFiccional))
        FILTER(?tipoLinha IN (:LinhaOriginal, :LinhaAlternativa))
        OPTIONAL{{ 
        :{id_livro} :refereEvento ?evento }}
        OPTIONAL {{ ?evento :designacao ?nomeEvento }}
        OPTIONAL {{ ?evento :descricao ?eventoDesc }}
        OPTIONAL{{ :{id_livro} :titulo ?titulo }}
        BIND(STRAFTER(STR(?tipoLivro), '#') AS ?livroTipo)
        BIND(STRAFTER(STR(?tipoLinha), '#') AS ?LinhaTipo)
        BIND(STRAFTER(STR(?linha), '#') AS ?Linha)
        BIND(STRAFTER(STR(?evento), '#') AS ?Evento)
    }}
    """
    res = execute_query(q)
    if not res or not res["results"]["bindings"]:
        return "Livro não encontrado", 404
    
    rows = res['results']['bindings']
    first = rows[0]
    
    livro = {
        "id": id_livro,
        "titulo": first.get("titulo", {}).get("value", "Título Desconhecido"),
        "tipo": first.get("livroTipo", {}).get("value", ""),
        "autor": first.get("nomeAutor", {}).get("value", ""),
        "pais": first.get("paisOri", {}).get("value", ""),
        "linhas": {},
        "eventos": {}
    }

    for row in rows:
        if "Linha" in row:
            line = row["Linha"]["value"]
            if line not in livro["linhas"]:
                livro["linhas"][line] = {
                    "id" : line,
                    "tipo": row["LinhaTipo"]["value"]
                }
        if "Evento" in row:
            event = row["Evento"]["value"]
            if event not in livro["eventos"]:
                livro['eventos'][event] = {
                    "id" : event,
                    "nome" : row.get("nomeEvento",{}).get("value", ""),
                    "descricao" : row.get("eventoDesc",{}).get("value", "")
                }
          
    return render_template("livro.html", livro = livro)

@app.route('/eventos')
def eventosRoute():
    q= """
    PREFIX : <http://example.org/biblioteca-temporal#>
    SELECT ?eventoId ?eventoTipo ?designacao ?descricao ?Livro WHERE {
        ?idEvento a ?tipoEvento ;
        Filter(?tipoEvento IN (:EventoHistorico, :EventoFuturo, :Evento))
        Optional {?idEvento :designacao ?designacao ;}
        Optional {?idEvento :descricao ?descricao .}
        ?livro a :Livro ;
            :refereEvento ?idEvento .
        BIND(STRAFTER(STR(?idEvento), "#") AS ?eventoId)
        BIND(STRAFTER(STR(?tipoEvento), "#") AS ?eventoTipo)
        BIND(STRAFTER(STR(?livro), "#") AS ?Livro)
    }   
    """
    res = execute_query(q)
    livro = {}
    if not res or not res["results"]["bindings"]:
        return "Eventos não encontrados", 404

    eventos = res['results']['bindings'] 
    for evento in eventos:
        evento1 = evento['eventoId']['value']
        if evento1 not in livro:
            livro[evento1] = {
                "Id": evento.get("eventoId", {}).get("value", "Id Desconhecido"),
                "Tipo": evento["eventoTipo"]["value"],
                "Designação": [],
                "Descrição": set(),
                "Livros": set(),
            }
    
        if evento['designacao']['value']:
            livro[evento1]["Designação"] = evento["designacao"]["value"],
        if evento['descricao']['value']:
            if evento['descricao']['value'] not in livro[evento1]['Descrição']:
                livro[evento1]["Descrição"].add(evento['descricao']['value'])
        if evento['Livro']['value'] not in livro[evento1]['Livros']:
            livro[evento1]["Livros"].add(evento['Livro']['value'])

    return render_template("eventos.html", livros = livro)

@app.route('/linhas')
def linhasTRoute():
    q= """
    PREFIX : <http://example.org/biblioteca-temporal#>
    select ?linhaID ?LinhaTipo where {
        ?linha a ?tipoLinha .
        FILTER(?tipoLinha in (:LinhaOriginal, :LinhaAlternativa))
        BIND(STRAFTER(STR(?linha), '#') AS ?linhaID)
        BIND(STRAFTER(STR(?tipoLinha), '#') AS ?LinhaTipo)
    }
    """
    lines = {}
    res = execute_query(q)
    if not res or not res["results"]["bindings"]:
        return "Eventos não encontrados", 404

    linhas = res['results']['bindings'] 
    for linha in linhas:
        linhaId = linha['linhaID']['value']
        lines[linhaId] = {
            "Linha_Id": linhaId,
            "Tipo_de_Linha": linha["LinhaTipo"]["value"]
        }

    return render_template("linhas.html", lines=lines)

@app.route('/linha/<linhaID>')
def linhaRoute(linhaID):
    q= f"""
    PREFIX : <http://example.org/biblioteca-temporal#>
    select ?LinhaTipo (GROUP_CONCAT(?livros; separator=",") AS ?Livros) (GROUP_CONCAT(?titulo; separator="|") AS ?Titulo) (GROUP_CONCAT(?tipo_Livro; separator=", ") AS ?LivroTipo) where {{
                :{linhaID} a ?tipoLinha .
                ?livro :existeEm :{linhaID} ;
                OPTIONAL {{ ?livro :titulo ?titulo }}
                ?livro a ?tipoLivro .
                FILTER(?tipoLinha in (:LinhaOriginal, :LinhaAlternativa))
                        
                FILTER(?tipoLivro in (:LivroParadoxal, :LivroHistorico, :LivroFiccional))
                BIND(STRAFTER(STR(?livro), '#') AS ?livros)
                BIND(STRAFTER(STR(?tipoLinha), '#') AS ?LinhaTipo)
                BIND(STRAFTER(STR(?tipoLivro), '#') AS ?tipo_Livro)
        }} group by ?LinhaTipo
    """
    line = {}
    res = execute_query(q)
    if not res or not res["results"]["bindings"]:
        return "Eventos não encontrados", 404

    linha = res['results']['bindings'] 
    for info in linha:
        line[linhaID] = {
            "Linha_Id": linhaID,
            "Tipo_de_Linha": info["LinhaTipo"]["value"],
            "Livros_Existentes": {}
        }
        info["Livros"]["value"] = info["Livros"]["value"].split(",")
        info["Titulo"]["value"] = info["Titulo"]["value"].split("|")
        info["LivroTipo"]["value"] = info["LivroTipo"]["value"].split(",")
        
        for i in range(len(info["Livros"]["value"])):
            Id = info["Livros"]["value"][i]
            line[linhaID]["Livros_Existentes"][Id] = {
                "Livro": info["Livros"]["value"][i],
                "Titulo": info["Titulo"]["value"][i],
                "Tipo_De_Livro": info["LivroTipo"]["value"][i]
            }    
    return render_template("linha.html", line=line)

if __name__ == '__main__':
    app.run(debug = True)