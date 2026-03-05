import json
from rdflib import Graph, Namespace, RDF, URIRef, Literal

# Namespace
EX = Namespace("http://www.semanticweb.org/guilhermepinho/ontologies/2026/2/bibliotecas")

# Criar grafo
g = Graph()
g.parse("biblioteca_Temporal.ttl", format="turtle")
g.bind("", EX)

def importI(file): 
    # Carregar JSON
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

    for item in data:
        subject = EX[item["id"]]

        # Tipo (classe)
        if "tipo" in item:
            g.add((subject, RDF.type, EX[item["tipo"]]))

        # TrabalhaEm
        if "trabalhaEm" in item:
            g.add((subject, EX.trabalhaEm, EX[item["trabalhaEm"]]))

        # EscritoPor
        if "escritoPor" in item:
            g.add((subject, EX.escritoPor, EX[item["escritoPor"]]))

        # PertenceA
        if "pertenceA" in item:
            g.add((subject, EX.pertenceA, EX[item["pertenceA"]]))

        # RefereEvento
        if "refereEvento" in item:
            g.add((subject, EX.refereEvento, EX[item["refereEvento"]]))

        # Nome (literal)
        if "nome" in item:
            g.add((subject, EX.nome, Literal(item["nome"])))

        # ExisteEm (pode ser lista ou string)
        if "existeEm" in item:
            if isinstance(item["existeEm"], list):
                for linha in item["existeEm"]:
                    g.add((subject, EX.existeEm, EX[linha]))
            else:
                g.add((subject, EX.existeEm, EX[item["existeEm"]]))

importI("dataset_temporal_100.json")
importI("dataset_temporal_v2_100.json")

# Guardar novamente TTL
g.serialize(destination="biblioteca_Temporal_Povoada.ttl", format="turtle")

print("Importação concluída com sucesso.")