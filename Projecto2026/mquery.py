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
query= f"""
 PREFIX : <http://www.semanticweb.org/guilhermepinho/ontologies/2026/3/monumentosPT/>
    SELECT Distinct ?NameMon ?subNomes ?normaType ?Year ?tipo ?lat ?long ?img ?nregiao ?ndistrito ?NameConc ?NameFreg ?descricao WHERE {{
        :mon_74628 a ?tipoMonumento ;
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
        
        OPTIONAL {{ :mon_74628 :temTipologia ?tipo . }}
        OPTIONAL {{ :mon_74628 :temLatitude ?lat . }}
        OPTIONAL {{ :mon_74628 :temLongitude ?long . }}
        OPTIONAL {{ :mon_74628 :temImagemURL ?img . }}
        OPTIONAL {{ :mon_74628 :Ano_Fundacao ?Year . }}
        OPTIONAL {{ :mon_74628 :temOutrosNomes ?subNomes . }}
        OPTIONAL {{ :mon_74628 :temDescricao ?descricao . }}

        BIND(STRAFTER(str(?tipoMonumento), "monumentosPT/") as ?normaType)
        FILTER(?normaType != "Monumento" && ?normaType != "NamedIndividual" && ?normaType != "")

    }}"""
res = execute_query(query)

import json
f_out = open("res.json", "w")
json.dump(res, f_out, indent=4, ensure_ascii=False)