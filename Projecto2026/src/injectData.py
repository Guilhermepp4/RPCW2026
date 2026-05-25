import json
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, XSD
import re

g = Graph()
g.parse("../Ontologias/finalmonumentosPT.ttl", format="turtle") 

PREFIX_URI = "http://www.semanticweb.org/guilhermepinho/ontologies/2026/3/monumentosPT/"
NS = Namespace(PREFIX_URI)

prop_descricao = NS.temDescricao
prop_outros_nomes = NS.temOutrosNomes

print("A injetar dados na ontologia...")

with open("../datasets_finished/monumentosDescricao.json", "r", encoding='utf-8') as f:
    dados = json.load(f)

contagem = 0

distritos = dados.get("Distritos", {})
for distrito, info_distrito in distritos.items():
    concelhos = info_distrito.get("Concelhos", {})
    
    for nome_concelho, lista_monumentos in concelhos.items():
        for mon in lista_monumentos:            
            id_monumento = mon.get("ID")

            if not id_monumento:
                print(f"ID ausente para um monumento em {nome_concelho}, distrito {distrito}. A saltar...")
                continue

            uri_monumento = URIRef(PREFIX_URI + "mon_" + id_monumento)

            if mon.get("Outros_Nomes"):
                outros_nomes = mon["Outros_Nomes"]
                g.add((uri_monumento, prop_outros_nomes, Literal(outros_nomes, lang="pt")))
            
            if mon.get("Descrição"):
                descricao = mon["Descrição"]
                descricao_limpa = re.sub(r"\(\s*ver\s*[^)]*\s*\)", "", descricao, flags=re.IGNORECASE)
                descricao_limpa = re.sub(r"\s+", " ", descricao_limpa).strip()
                
                g.add((uri_monumento, prop_descricao, Literal(descricao_limpa, lang="pt")))

print(f"Sucesso! {contagem} monumentos atualizados.")
print("A guardar o ficheiro OWL final...")

g.serialize(destination="../Ontologias/finalmonumentosPT_atualizada.ttl", format="turtle")

print("Ontologia guardada com sucesso!")