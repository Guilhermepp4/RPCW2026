import json

ALUNO_ID = "PG60263"
BASE_IRI = f"http://www.di.uminho.pt/rpcw2026/{ALUNO_ID}"

PREFIXES = f"""@prefix : <{BASE_IRI}#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@base <{BASE_IRI}> .

<{BASE_IRI}> a owl:Ontology .
"""

ESTRUTURA_BASE = """
#################################################################
#    Classes [cite: 149]
#################################################################

###  Classes Base [cite: 124, 128]
:Jogo a owl:Class .
:Autor a owl:Class .
:Editora a owl:Class .
:Mecanica a owl:Class .
:Premio a owl:Class .


#################################################################
#    Object Properties [cite: 151]
#################################################################

###  Relações entre Classes [cite: 129, 131]
:designedGame a owl:ObjectProperty ;
              rdfs:domain :Autor ;
              rdfs:range :Jogo .

:publishedGame a owl:ObjectProperty ;
               rdfs:domain :Editora ;
               rdfs:range :Jogo .

:usedInGame a owl:ObjectProperty ;
            rdfs:domain :Mecanica ;
            rdfs:range :Jogo .

:wonByGame a owl:ObjectProperty ;
           rdfs:domain :Premio ;
           rdfs:range :Jogo .


#################################################################
#    Data Properties [cite: 150]
#################################################################

###  Atributos das Classes [cite: 129, 130]
:name a owl:DatatypeProperty ;
      rdfs:range xsd:string .

:category a owl:DatatypeProperty ;
          rdfs:domain :Jogo ;
          rdfs:range xsd:string .

:minPlayers a owl:DatatypeProperty ;
            rdfs:domain :Jogo ;
            rdfs:range xsd:integer .

:maxPlayers a owl:DatatypeProperty ;
            rdfs:domain :Jogo ;
            rdfs:range xsd:integer .

:playingTimeMinutes a owl:DatatypeProperty ;
                    rdfs:domain :Jogo ;
                    rdfs:range xsd:integer .

:descriptionEN a owl:DatatypeProperty ;
               rdfs:domain :Jogo ;
               rdfs:range xsd:string .

:country a owl:DatatypeProperty ;
         rdfs:domain :Editora ;
         rdfs:range xsd:string .

:year a owl:DatatypeProperty ;
      rdfs:domain :Premio ;
      rdfs:range xsd:integer .
"""

with open("boardgames_base.ttl", "w", encoding="utf-8") as f:
    f.write(PREFIXES + ESTRUTURA_BASE)
print("-> Ficheiro 'boardgames_base.ttl' gerado.")


print("A processar os ficheiros JSON para povoamento...")

def carregar_json(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Aviso: {filename} não encontrado.")
        return []

def safe_str(text):
    return text.replace('"', '\\"')

corpo_individuos = """
#################################################################
#    Individuals
#################################################################
"""

jogos_data = carregar_json('jogos.json')
for jogo in jogos_data:
    corpo_individuos += f"""
###  {BASE_IRI}#{jogo['id']}
:{jogo['id']} a :Jogo ;
      :name "{safe_str(jogo['name'])}"^^xsd:string ;
      :category "{safe_str(jogo['category'])}"^^xsd:string ;
      :minPlayers {jogo['minPlayers']} ;
      :maxPlayers {jogo['maxPlayers']} ;
      :playingTimeMinutes {jogo['playingTimeMinutes']} ;
      :descriptionEN "{safe_str(jogo['descriptionEN'])}"^^xsd:string .
"""

autores_data = carregar_json('autores.json')
for autor in autores_data:
    relacoes = ""
    for jogo_id in autor.get('designedGames', []):
        relacoes += f" ;\n      :designedGame :{jogo_id}"
    
    corpo_individuos += f"""
###  {BASE_IRI}#{autor['id']}
:{autor['id']} a :Autor ;
      :name "{safe_str(autor['name'])}"^^xsd:string{relacoes} .
"""

editoras_data = carregar_json('editoras.json')
if isinstance(editoras_data, dict):
    editoras_data = [editoras_data]

for editora in editoras_data:
    relacoes = ""
    for jogo_id in editora.get('publishedGames', []):
        relacoes += f" ;\n      :publishedGame :{jogo_id}"
        
    corpo_individuos += f"""
###  {BASE_IRI}#{editora['id']}
:{editora['id']} a :Editora ;
      :name "{safe_str(editora['name'])}"^^xsd:string ;
      :country "{safe_str(editora['country'])}"^^xsd:string{relacoes} .
"""

mecanicas_data = carregar_json('mecanicas.json')
for mec in mecanicas_data:
    relacoes = ""
    for jogo_id in mec.get('usedInGames', []):
        relacoes += f" ;\n      :usedInGame :{jogo_id}"
        
    corpo_individuos += f"""
###  {BASE_IRI}#{mec['id']}
:{mec['id']} a :Mecanica ;
      :name "{safe_str(mec['name'])}"^^xsd:string{relacoes} .
"""

premios_data = carregar_json('premios.json')
for premio in premios_data:
    corpo_individuos += f"""
###  {BASE_IRI}#{premio['id']}
:{premio['id']} a :Premio ;
      :name "{safe_str(premio['name'])}"^^xsd:string ;
      :year {premio['year']} ;
      :wonByGame :{premio['wonByGame']} .
"""

with open("boardgames_ind.ttl", "w", encoding="utf-8") as f:
    f.write(PREFIXES + ESTRUTURA_BASE + corpo_individuos)
    
print("-> Ficheiro 'boardgames_ind.ttl' gerado com a sintaxe limpa ('a')!")