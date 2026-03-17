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
q= """
PREFIX : <http://example.org/biblioteca-temporal#>
select ?LinhaTipo (GROUP_CONCAT(?livros; separator=", ") AS ?Livros) (GROUP_CONCAT(?titulo; separator="| ") AS ?Titulo) (GROUP_CONCAT(?tipo_Livro; separator=", ") AS ?LivroTipo) where {
            ?linhaID a ?tipoLinha .
            ?livro :existeEm ?linhaID ;
        	OPTIONAL { ?livro :titulo ?titulo }
            ?livro a ?tipoLivro .
        	FILTER(?tipoLinha in (:LinhaOriginal, :LinhaAlternativa))
                    
            FILTER(?tipoLivro in (:LivroParadoxal, :LivroHistorico, :LivroFiccional))
            BIND(STRAFTER(STR(?livro), '#') AS ?livros)
            BIND(STRAFTER(STR(?tipoLinha), '#') AS ?LinhaTipo)
            BIND(STRAFTER(STR(?tipoLivro), '#') AS ?tipo_Livro)
    } group by ?LinhaTipo
"""
res = execute_query(q)

import json
f_out = open("res.json", "w")
json.dump(res, f_out, indent=4, ensure_ascii=False)