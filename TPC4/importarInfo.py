import json
from rdflib import Graph, Namespace, RDF, URIRef, Literal

# namespace da ontologia
BASE = "http://rpcw.di.uminho.pt/2026/untitled-ontology-13/"
ONT = Namespace(BASE)

g = Graph()
g.parse("bibliotecatemporal.ttl", format="turtle")

g.bind("", ONT)


# mapeamento de tipos JSON -> classes da ontologia
class_map = {
    "LivroHistorico": "LivroHistórico",
    "EventoHistorico": "EventoHistórico"
}


def get_class(tipo):
    if tipo in class_map:
        return ONT[class_map[tipo]]
    return ONT[tipo]


def process_dataset(file):

    with open(file, encoding="utf-8") as f:
        data = json.load(f)

    for item in data:

        subj = ONT[item["id"]]

        # classe
        classe = get_class(item["tipo"])
        g.add((subj, RDF.type, classe))

        # nome literal
        if "nome" in item:
            g.add((subj, ONT.nome, Literal(item["nome"])))

        # bibliotecario trabalha em biblioteca
        if "trabalhaEm" in item:
            g.add((subj, ONT.trabalhaEm, ONT[item["trabalhaEm"]]))

        # livro -> autor
        if "escritoPor" in item:
            g.add((subj, ONT.escritoPor, ONT[item["escritoPor"]]))

        # livro pertence a biblioteca
        if "pertenceA" in item:
            g.add((subj, ONT.pertenceA, ONT[item["pertenceA"]]))

        # livro refere evento
        if "refereEvento" in item:
            g.add((subj, ONT.refere, ONT[item["refereEvento"]]))

        # existeEm pode ser lista
        if "existeEm" in item:

            val = item["existeEm"]

            if isinstance(val, list):
                for v in val:
                    g.add((subj, ONT.existeEm, ONT[v]))
            else:
                g.add((subj, ONT.existeEm, ONT[val]))


# processar datasets
process_dataset("dataset_temporal_100.json")
process_dataset("dataset_temporal_v2_100.json")


# guardar resultado
g.serialize("bibliotecaTemporalFinal.ttl", format="turtle")

print("Ontologia povoada criada: bibliotecaTemporalFinal.ttl")