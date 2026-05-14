import json
import re
import unicodedata

def limpar_uri(txt):
    txt = txt.lower().strip()

    txt = unicodedata.normalize('NFD', txt)
    txt = txt.encode('ascii', 'ignore').decode('utf-8')

    txt = txt.replace(" ", "_")
    txt = re.sub(r'[^a-z0-9_]', '', txt)

    return txt


with open("datasest_finished/universidades.json", encoding="utf-8") as f:
    data = json.load(f)

ttl_content = f"""@prefix : <http://www.semanticweb.org/guilhermepinho/ontologies/2026/3/turismo/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@base <http://www.semanticweb.org/guilhermepinho/ontologies/2026/3/turismo/> .

<http://www.semanticweb.org/guilhermepinho/ontologies/2026/3/turismo> rdf:type owl:Ontology .

#################################################################
#    Object Properties
#################################################################

###  http://www.semanticweb.org/guilhermepinho/ontologies/2026/3/turismo/pertenceA_Regiao
:pertenceA_Regiao rdf:type owl:ObjectProperty ;
                  rdfs:domain :Distrito ;
                  rdfs:range :Região .


###  http://www.semanticweb.org/guilhermepinho/ontologies/2026/3/turismo/pertenceA_Universidade
:pertenceA_Universidade rdf:type owl:ObjectProperty ;
                        rdfs:domain :Escola ;
                        rdfs:range :Tipo .


###  http://www.semanticweb.org/guilhermepinho/ontologies/2026/3/turismo/pertence_Distrito
:pertence_Distrito rdf:type owl:ObjectProperty ;
                   rdfs:domain :Escola ;
                   rdfs:range :Distrito .


###  http://www.semanticweb.org/guilhermepinho/ontologies/2026/3/turismo/temEscola
:temEscola rdf:type owl:ObjectProperty ;
           rdfs:domain :Tipo ;
           rdfs:range :Escola .

###  http://www.semanticweb.org/guilhermepinho/ontologies/2026/3/turismo/pertenceArquipelago
:pertenceArquipelago rdf:type owl:ObjectProperty ;
                     owl:inverseOf :temIlha .

#################################################################
#    Data properties
#################################################################

###  http://www.semanticweb.org/guilhermepinho/ontologies/2026/3/turismo/nome
:nome rdf:type owl:DatatypeProperty ;
      rdfs:domain [ rdf:type owl:Class ;
                    owl:unionOf ( :Distrito
                                  :Escola
                                  :Região
                                  :Tipo
                                )
                  ] ;
      rdfs:range xsd:string .


###  http://www.semanticweb.org/guilhermepinho/ontologies/2026/3/turismo/tem_Natureza
:tem_Natureza rdf:type owl:DatatypeProperty ;
              rdfs:domain :Escola ;
              rdfs:range xsd:string .


###  http://www.semanticweb.org/guilhermepinho/ontologies/2026/3/turismo/tem_Tipo
:tem_Tipo rdf:type owl:DatatypeProperty ;
          rdfs:domain :Escola ;
          rdfs:range xsd:string .


#################################################################
#    Classes
#################################################################

###  http://www.semanticweb.org/guilhermepinho/ontologies/2026/3/turismo#Estabelecimento
:Estabelecimento rdf:type owl:Class .


###  http://www.semanticweb.org/guilhermepinho/ontologies/2026/3/turismo#Politécnico
:Politécnico rdf:type owl:Class ;
             owl:equivalentClass [ owl:intersectionOf ( :Tipo
                                                        [ rdf:type owl:Restriction ;
                                                          owl:onProperty :tem_Tipo ;
                                                          owl:hasValue "Politécnico"
                                                        ]
                                                      ) ;
                                   rdf:type owl:Class
                                 ] .


###  http://www.semanticweb.org/guilhermepinho/ontologies/2026/3/turismo#Privada
:Privada rdf:type owl:Class ;
         owl:equivalentClass [ owl:intersectionOf ( :Escola
                                                    [ rdf:type owl:Restriction ;
                                                      owl:onProperty :tem_Natureza ;
                                                      owl:hasValue "Privada"
                                                    ]
                                                  ) ;
                               rdf:type owl:Class
                             ] .


###  http://www.semanticweb.org/guilhermepinho/ontologies/2026/3/turismo#Publica
:Publica rdf:type owl:Class ;
         owl:equivalentClass [ owl:intersectionOf ( :Escola
                                                    [ rdf:type owl:Restriction ;
                                                      owl:onProperty :tem_Natureza ;
                                                      owl:hasValue "Pública"
                                                    ]
                                                  ) ;
                               rdf:type owl:Class
                             ] .


###  http://www.semanticweb.org/guilhermepinho/ontologies/2026/3/turismo#Universidade
:Universidade rdf:type owl:Class ;
              owl:equivalentClass [ owl:intersectionOf ( :Tipo
                                                         [ rdf:type owl:Restriction ;
                                                           owl:onProperty :tem_Tipo ;
                                                           owl:hasValue "Universidade"
                                                         ]
                                                       ) ;
                                    rdf:type owl:Class
                                  ] .


###  http://www.semanticweb.org/guilhermepinho/ontologies/2026/3/turismo/Distrito
:Distrito rdf:type owl:Class .


###  http://www.semanticweb.org/guilhermepinho/ontologies/2026/3/turismo/Escola
:Escola rdf:type owl:Class ;
        rdfs:subClassOf :Estabelecimento .


###  http://www.semanticweb.org/guilhermepinho/ontologies/2026/3/turismo/Região
:Região rdf:type owl:Class .


###  http://www.semanticweb.org/guilhermepinho/ontologies/2026/3/turismo/Tipo
:Tipo rdf:type owl:Class ;
      rdfs:subClassOf :Estabelecimento .


###  Generated by the OWL API (version 4.5.29.2024-05-13T12:11:03Z) https://github.com/owlcs/owlapi

#################################################################
#    Indivíduos
#################################################################

### Regiões

"""
regioes_vistas = set()

for esc in data["Escolas"]:
    reg = esc["Região"]

    if reg in regioes_vistas:
        continue

    regioes_vistas.add(reg)

    reg_uri = "reg_" + limpar_uri(reg)

    ttl_content += f"""
:{reg_uri} a :Região ;
    :nome "{reg}" .
"""
    
distritos_vistos = set()

ttl_content += '\n### DISTRITOS\n'
for escola in data['Escolas']:
    nome_dist = escola["Distrito"]
    clean_name = limpar_uri(nome_dist)

    if nome_dist in distritos_vistos:
        continue
    distritos_vistos.add(nome_dist)

    if "madeira" in clean_name or "acores" in clean_name:
        uri = f"arq_{clean_name}"
    else:
        uri = f"dist_{clean_name}"

    reg = f"reg_{limpar_uri(escola['Região'])}"

    ttl_content += f"""
:{uri} a :Distrito ;
    :nome "{escola["Distrito"]}" ;
    :pertenceA_Regiao :{reg} .
    """
ttl_content += '\n### ESCOLAS\n'
# ESCOLAS
for esc in data["Escolas"]:
    inst = esc["Instituicao"]

    uni_id = data["Universidades"][inst]["id"]
    uni_uri = f"uni_{uni_id}"
    uri = "esc_" + limpar_uri(esc["Nome"]) + f"_{uni_uri}"
    
    nome_dist2 = esc["Distrito"]
    dist_id = limpar_uri(nome_dist2)
    if "madeira" in dist_id or "acores" in dist_id:
        dist_uri = f"arq_{dist_id}"
    else:
        dist_uri = f"dist_{dist_id}"
    
    natureza_escola = f"Privada" if esc["Natureza"] == "Privada" else "Publica"
    tipo_escola = "Politécnico" if esc["Tipo"] == "Politécnico" else "Universidade"
    tipo_rdf = f"""rdf:type owl:NamedIndividual , 
                    [ owl:intersectionOf ( :{natureza_escola}
                                        :{tipo_escola} 
                    ) ; 
                    rdf:type owl:Class 
                ]"""
    ttl_content += f"""
:{uri} {tipo_rdf} ;
    :nome "{esc["Nome"]}" ;
    :pertenceA_Universidade :{uni_uri} ;
    """
    if "madeira" in dist_uri or "acores" in dist_uri:
        ttl_content += f""":pertenceArquipelago :{dist_uri} ;"""
    else:
        ttl_content += f""":pertence_Distrito :{dist_uri} ;"""
        

    ttl_content += f"""
    :tem_Tipo "{esc["Tipo"]}" ;
    :tem_Natureza "{esc["Natureza"]}" .
    """
ttl_content += '\n### UNIVERSIDADES\n'

# UNIVERSIDADES
for nome, uni in data["Universidades"].items():
    uni_id = uni['id']

    escolas = [esc for esc in data["Escolas"] if esc["Instituicao"] == nome]
    ttl_content += f"""
:uni_{uni_id} a :Universidade ;
    :nome "{uni['Nome']}" ;
"""
    for i, esc in enumerate(escolas):
        esc_id = limpar_uri(esc['Nome'])
        if i == len(escolas) - 1:
            ttl_content += f"   :temEscola :esc_{esc_id}_uni_{uni_id} .\n"
        else:
            ttl_content += f"   :temEscola :esc_{esc_id}_uni_{uni_id} ;\n"


with open("ensino.ttl", "w", encoding="utf-8") as f:
    f.write(ttl_content)

print("TTL criado com sucesso!")