import json
import re
import unicodedata

def extrair_coordenadas(coord_str):
    if not coord_str or not isinstance(coord_str, str):
        return "None", "None"
    
    # Procura por todos os números (decimais ou inteiros) na string
    numeros = re.findall(r"\d+\.\d+", coord_str)
    
    if len(numeros) >= 2:
        lat = numeros[0]
        lon = numeros[1]
        
        # Lógica para Oeste (O/W) e Sul (S) serem negativos
        if "O" in coord_str or "W" in coord_str:
            lon = f"-{lon}"
        if "S" in coord_str:
            lat = f"-{lat}"
            
        return lat, lon
    return "None", "None"

def limpar_uri(txt):
    txt = txt.lower().strip()

    txt = unicodedata.normalize('NFD', txt)
    txt = txt.encode('ascii', 'ignore').decode('utf-8')

    txt = txt.replace(" ", "_")
    txt = re.sub(r'[^a-z0-9_]', '', txt)

    return txt

def obter_classe_monumento(categoria_json):
    cat = categoria_json.lower()
    
    mapeamento = {
        "mista": "ArquiteturaMista",
        "religios": "EdificioReligioso",
        "militar": "EstruturaMilitar",
        "arqueo": "SitioArqueologico",
        "escul": "SitioArqueologico"
    }
    
    if any(palavra in cat for palavra in ["civil", "industrial", "teatro"]):
        return "MonumentoCivil"
    
    for chave, classe in mapeamento.items():
        if chave in cat:
            return classe
            
    return "Monumento"


with open("datasest_finished/monumentos.json", encoding="utf-8") as f:
    data = json.load(f)

ttl_content = f"""@prefix : <http://www.semanticweb.org/guilhermepinho/ontologies/2026/3/monumentosPT/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@base <http://www.semanticweb.org/guilhermepinho/ontologies/2026/3/monumentosPT/> .

<http://www.semanticweb.org/guilhermepinho/ontologies/2026/3/monumentosPT> rdf:type owl:Ontology .

#################################################################
#    Object Properties
#################################################################

###  http://www.semanticweb.org/guilhermepinho/ontologies/2026/3/monumentosPT#pertenceArquipelago
:pertenceArquipelago rdf:type owl:ObjectProperty ;
                     owl:inverseOf :temIlha .


###  http://www.semanticweb.org/guilhermepinho/ontologies/2026/3/monumentosPT#pertenceIlha
:pertenceIlha rdf:type owl:ObjectProperty ;
              rdfs:domain :Concelho ;
              rdfs:range :Ilha .


###  http://www.semanticweb.org/guilhermepinho/ontologies/2026/3/monumentosPT#temIlha
:temIlha rdf:type owl:ObjectProperty ;
         rdfs:domain :Arquipelago ;
         rdfs:range :Ilha .


###  http://www.semanticweb.org/guilhermepinho/ontologies/2026/3/monumentosPT/ConcelhoTemMon
:ConcelhoTemMon rdf:type owl:ObjectProperty ;
                owl:inverseOf :ficaEmConcelho .


###  http://www.semanticweb.org/guilhermepinho/ontologies/2026/3/monumentosPT/FreguesiaTemMon
:FreguesiaTemMon rdf:type owl:ObjectProperty ;
                 owl:inverseOf :ficaEmFreguesia .


###  http://www.semanticweb.org/guilhermepinho/ontologies/2026/3/monumentosPT/ficaEmConcelho
:ficaEmConcelho rdf:type owl:ObjectProperty ;
                rdfs:domain :Monumento ;
                rdfs:range :Concelho .


###  http://www.semanticweb.org/guilhermepinho/ontologies/2026/3/monumentosPT/ficaEmFreguesia
:ficaEmFreguesia rdf:type owl:ObjectProperty ;
                 rdfs:domain :Monumento ;
                 rdfs:range :Freguesia .


###  http://www.semanticweb.org/guilhermepinho/ontologies/2026/3/monumentosPT/pertence_Distrito
:pertence_Distrito rdf:type owl:ObjectProperty ;
                   rdfs:domain :Concelho ;
                   rdfs:range :Distrito .


###  http://www.semanticweb.org/guilhermepinho/ontologies/2026/3/monumentosPT/pertence_concelho
:pertence_concelho rdf:type owl:ObjectProperty ;
                   owl:inverseOf :temFreguesia .


###  http://www.semanticweb.org/guilhermepinho/ontologies/2026/3/monumentosPT/temConcelho
:temConcelho rdf:type owl:ObjectProperty ;
             rdfs:domain [ rdf:type owl:Class ;
                           owl:unionOf ( :Ilha
                                         :Distrito
                                       )
                         ] ;
             rdfs:range :Concelho .


###  http://www.semanticweb.org/guilhermepinho/ontologies/2026/3/monumentosPT/temFreguesia
:temFreguesia rdf:type owl:ObjectProperty .


#################################################################
#    Data properties
#################################################################

###  http://www.semanticweb.org/guilhermepinho/ontologies/2026/3/monumentosPT/Ano_Fundacao
:Ano_Fundacao rdf:type owl:DatatypeProperty ;
              rdfs:domain :Monumento ;
              rdfs:range xsd:string .


###  http://www.semanticweb.org/guilhermepinho/ontologies/2026/3/monumentosPT/Designacao
:Designacao rdf:type owl:DatatypeProperty ;
            rdfs:domain :Monumento ;
            rdfs:range xsd:string .


###  http://www.semanticweb.org/guilhermepinho/ontologies/2026/3/monumentosPT/nome
:nome rdf:type owl:DatatypeProperty ;
      rdfs:domain [ rdf:type owl:Class ;
                    owl:unionOf ( :Arquipelago
                                  :Ilha
                                  :Concelho
                                  :Distrito
                                  :Freguesia
                                  :Monumento
                                )
                  ] ;
      rdfs:range xsd:string .


###  http://www.semanticweb.org/guilhermepinho/ontologies/2026/3/monumentosPT/temImagemURL
:temImagemURL rdf:type owl:DatatypeProperty ;
              rdfs:domain :Monumento ;
              rdfs:range xsd:anyURI .


###  http://www.semanticweb.org/guilhermepinho/ontologies/2026/3/monumentosPT/temLatitude
:temLatitude rdf:type owl:DatatypeProperty ;
             rdfs:domain :Monumento ;
             rdfs:range xsd:decimal .


###  http://www.semanticweb.org/guilhermepinho/ontologies/2026/3/monumentosPT/temLongitude
:temLongitude rdf:type owl:DatatypeProperty ;
              rdfs:domain :Monumento ;
              rdfs:range xsd:decimal .


###  http://www.semanticweb.org/guilhermepinho/ontologies/2026/3/monumentosPT/temTipologia
:temTipologia rdf:type owl:DatatypeProperty ;
              rdfs:domain :Monumento ;
              rdfs:range xsd:string .


#################################################################
#    Classes
#################################################################

###  http://www.semanticweb.org/guilhermepinho/ontologies/2026/3/monumentosPT#Arquipelago
:Arquipelago rdf:type owl:Class .


###  http://www.semanticweb.org/guilhermepinho/ontologies/2026/3/monumentosPT#Ilha
:Ilha rdf:type owl:Class ;
      rdfs:subClassOf [ rdf:type owl:Restriction ;
                        owl:onProperty :pertenceArquipelago ;
                        owl:qualifiedCardinality "1"^^xsd:nonNegativeInteger ;
                        owl:onClass :Arquipelago
                      ] .


###  http://www.semanticweb.org/guilhermepinho/ontologies/2026/3/monumentosPT/ArquiteturaMista
:ArquiteturaMista rdf:type owl:Class ;
                  rdfs:subClassOf :Monumento .


###  http://www.semanticweb.org/guilhermepinho/ontologies/2026/3/monumentosPT/Concelho
:Concelho rdf:type owl:Class ;
          rdfs:subClassOf [ rdf:type owl:Class ;
                            owl:unionOf ( [ rdf:type owl:Restriction ;
                                            owl:onProperty :pertenceIlha ;
                                            owl:qualifiedCardinality "1"^^xsd:nonNegativeInteger ;
                                            owl:onClass :Ilha
                                          ]
                                          [ rdf:type owl:Restriction ;
                                            owl:onProperty :pertence_Distrito ;
                                            owl:qualifiedCardinality "1"^^xsd:nonNegativeInteger ;
                                            owl:onClass :Distrito
                                          ]
                                        )
                          ] .


###  http://www.semanticweb.org/guilhermepinho/ontologies/2026/3/monumentosPT/Distrito
:Distrito rdf:type owl:Class .


###  http://www.semanticweb.org/guilhermepinho/ontologies/2026/3/monumentosPT/EdificioReligioso
:EdificioReligioso rdf:type owl:Class ;
                   rdfs:subClassOf :Monumento .


###  http://www.semanticweb.org/guilhermepinho/ontologies/2026/3/monumentosPT/EstruturaMilitar
:EstruturaMilitar rdf:type owl:Class ;
                  rdfs:subClassOf :Monumento .


###  http://www.semanticweb.org/guilhermepinho/ontologies/2026/3/monumentosPT/Freguesia
:Freguesia rdf:type owl:Class ;
           rdfs:subClassOf [ rdf:type owl:Restriction ;
                             owl:onProperty :pertence_concelho ;
                             owl:qualifiedCardinality "1"^^xsd:nonNegativeInteger ;
                             owl:onClass :Concelho
                           ] .


###  http://www.semanticweb.org/guilhermepinho/ontologies/2026/3/monumentosPT/Monumento
:Monumento rdf:type owl:Class ;
           rdfs:subClassOf [ rdf:type owl:Class ;
                             owl:unionOf ( [ rdf:type owl:Restriction ;
                                             owl:onProperty :ficaEmConcelho ;
                                             owl:someValuesFrom :Concelho
                                           ]
                                           [ rdf:type owl:Restriction ;
                                             owl:onProperty :ficaEmFreguesia ;
                                             owl:someValuesFrom :Freguesia
                                           ]
                                         )
                           ] .


###  http://www.semanticweb.org/guilhermepinho/ontologies/2026/3/monumentosPT/MonumentoCivil
:MonumentoCivil rdf:type owl:Class ;
                rdfs:subClassOf :Monumento .


###  http://www.semanticweb.org/guilhermepinho/ontologies/2026/3/monumentosPT/SitioArqueologico
:SitioArqueologico rdf:type owl:Class ;
                   rdfs:subClassOf :Monumento .


###  Generated by the OWL API (version 4.5.29.2024-05-13T12:11:03Z) https://github.com/owlcs/owlapi

#################################################################
#    Indivíduos
#################################################################

### Distritos
"""
freguesias_vistas = set()
monumentos_vistos = set()
maxId = 97017350

for distrito, conteudo_distrito in data["Distritos"].items():
    dist_uri = f"dist_{limpar_uri(distrito)}"

    ttl_content += f"""
:{dist_uri} a :Distrito ;
    :nome "{distrito}" .
"""
    for concelho, lista_monumentos in conteudo_distrito["Concelhos"].items():
        if concelho:
            concelho_uri = f"conc_{limpar_uri(concelho)}"
        else:
            concelho_uri = f"conc_desconecido"
        ttl_content += f"""
:{concelho_uri} a :Concelho ;
    :nome "{concelho}" ;
    :pertence_Distrito :{dist_uri} .
"""
        for mon in lista_monumentos:
            if mon["Freguesia"]:
                freguesia_nome = mon["Freguesia"]
            else:
                freguesia_nome = "Freguesia Desconhecida"
            freguesia_uri = f"freg_{limpar_uri(freguesia_nome)}"
            if freguesia_nome not in freguesias_vistas:
                ttl_content += f"""
:{freguesia_uri} a :Freguesia ;
    :nome "{freguesia_nome}" ;
    :pertence_concelho :{concelho_uri} .
        """
                freguesias_vistas.add(freguesia_nome)

            classes_encontradas = set()
            id_base = limpar_uri(mon['ID'])
            if id_base in monumentos_vistos:
                id_base += f"_{mon['Grau']}"
            monumentos_vistos.add(id_base)
            mon_uri = f"mon_{id_base}"
            lista_categrorias = mon["Categoria"].split("/")
            for cat in lista_categrorias:
                classe = obter_classe_monumento(cat)
                classes_encontradas.add(f":{classe}")
            if len(classes_encontradas) > 1 and "Monumento" in classes_encontradas:
                classes_encontradas.remove("Monumento")

            string_classes_unidas = " ".join(classes_encontradas)
            lat, lon = extrair_coordenadas(mon["Coordenadas"])

            if len(classes_encontradas) > 1:
                tipo_rdf = f"""rdf:type owl:NamedIndividual , 
                    [ owl:intersectionOf ( {string_classes_unidas} 
                    ) ; 
                    rdf:type owl:Class 
                ]"""
            else:
                tipo_rdf = f"a {string_classes_unidas}"
            
            ttl_content += f"""
:{mon_uri} {tipo_rdf} ;
    :nome "{mon['Designação'].replace('"', '\\"')}" ;"""
            if mon['Ano']:
                ttl_content += f"""
    :Ano_Fundacao "{mon['Ano']}" ;
    :temTipologia "{mon['Tipologia']}" ;"""
            if lat != "None" and lon != "None":
                ttl_content += f"""
    :temLatitude {lat} ;
    :temLongitude {lon} ;"""
            img_url = mon['Imagem'] if mon['Imagem'] else "http://www.sem-imagem.com"
            ttl_content += f"""
    :temImagemURL <{img_url}> ;"""
            ttl_content += f"""
    :ficaEmConcelho :{concelho_uri} ;
    :ficaEmFreguesia :{freguesia_uri} .
    """

for arquipelago, conteudo_arquipelago in data["Arquipelago"].items():
    arq_uri = f"arq_{limpar_uri(arquipelago)}"

    ttl_content += f"""
:{arq_uri} a :Arquipelago ;
    :nome "{arquipelago}" .
"""
    for ilha, lista_concelhos in conteudo_arquipelago["Ilha"].items():
        if ilha:
            ilha_uri = f"ilha_{limpar_uri(ilha)}"
        else:
            ilha_uri = f"ilha_desconecida"
        ttl_content += f"""
:{ilha_uri} a :Ilha ;
    :nome "{ilha}" ;
    :pertenceArquipelago :{arq_uri} .
"""
        for concelho, lista_monumentos in lista_concelhos["Concelhos"].items():
            if concelho:
                concelho_uri = f"conc_{limpar_uri(concelho)}"
            else:
                concelho_uri = "conc_desconecido"
            ttl_content += f"""
:{concelho_uri} a :Concelho ;
    :nome "{concelho}" ;
    :pertence_Ilha :{ilha_uri} .        
"""
            for mon in lista_monumentos:
                if mon["Freguesia"]:
                    freguesia_nome = mon["Freguesia"]
                else:
                    freguesia_nome = "Freguesia Desconhecida"
                freguesia_uri = f"freg_{limpar_uri(freguesia_nome)}"
                if freguesia_nome not in freguesias_vistas:
                    ttl_content += f"""
    :{freguesia_uri} a :Freguesia ;
        :nome "{freguesia_nome}" ;
        :pertence_concelho :{concelho_uri} .
            """
                    freguesias_vistas.add(freguesia_nome)

                if not mon['ID']:
                    id_base = str(maxId + 1)
                    maxId += 1
                else:
                    id_base = limpar_uri(mon['ID'])

                    if id_base in monumentos_vistos:
                        id_base += f"_{mon['Grau']}"
                
                monumentos_vistos.add(id_base)  
                mon_uri = f"mon_{id_base}"
                
                classe = obter_classe_monumento(mon['Categoria'])
                
                linhas_props = [f'a :{classe}']
                
                nome_esc = mon['Designação'].replace('"', '\\"')
                linhas_props.append(f':nome "{nome_esc}"')
                
                if mon.get('Ano'):
                    linhas_props.append(f':Ano_Fundacao "{mon["Ano"]}"')
                
                if mon.get('Tipologia'):
                    tipologia_esc = mon['Tipologia'].replace('"', '\\"')
                    linhas_props.append(f':temTipologia "{tipologia_esc}"')
                
                linhas_props.append(f':ficaEmFreguesia :{freguesia_uri}')
                linhas_props.append(f':ficaEmConcelho :{concelho_uri}')
                
                ttl_content += f"\n:{mon_uri} " + " ;\n    ".join(linhas_props) + " .\n"
with open("finalmonumentosPT.ttl", "w", encoding="utf-8") as f:
    f.write(ttl_content)

print("TTL criado com sucesso!")