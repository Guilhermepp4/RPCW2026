from SPARQLWrapper import SPARQLWrapper, JSON
import json

GRAPHDB_ENDPOINT = "http://localhost:7200/repositories/TurismoPT"

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
PREFIX : <http://www.semanticweb.org/guilhermepinho/ontologies/2026/3/monumentosPT/>
    SELECT DISTINCT ?id ?nome ?normaType ?ndistrito ?nconcelho ?nregiao ?lat ?long WHERE {
    
    ?m a ?tipoIndividuo ;
       :nome ?nome ;
       :ficaEmConcelho ?concelho .
    OPTIONAL { ?m :temLatitude ?lat . }
    OPTIONAL { ?m :temLongitude ?long . }
        
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
    }
    ORDER BY ?ndistrito ?nconcelho ?nome"""
res = execute_query(query)

import json
f_out = open("res.json", "w")
json.dump(res, f_out, indent=4, ensure_ascii=False)