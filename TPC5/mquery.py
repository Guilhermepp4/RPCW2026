from SPARQLWrapper import SPARQLWrapper, JSON
import json

GRAPHDB_ENDPOINT = "http://localhost:7200/repositories/biblioteca_temporal"

def execute_query(query):
    sparql = SPARQLWrapper(GRAPHDB_ENDPOINT)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    try:
        return sparql.query().convert()
    except Exception as e:
        print(f"Error executing query: {e}")
        return None
query= """
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
}"""
res = execute_query(query)

import json
f_out = open("res.json", "w")
json.dump(res, f_out, indent=4, ensure_ascii=False)