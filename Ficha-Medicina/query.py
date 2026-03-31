"""
Script 1: Povoa a ontologia com doenças, sintomas, descrições e tratamentos.

Entrada:  medical.ttl
          Disease_Syntoms.csv
          Disease_Description.csv
          Disease_Treatment.csv

Saída:    med_doencas.ttl     (doenças + sintomas + descrições)
          med_tratamentos.ttl (+ tratamentos)
"""

import csv
import re
from rdflib import Graph, Namespace, RDF, Literal

BASE = "http://www.example.org/disease-ontology#"
EX = Namespace(BASE)

def uri_safe(name: str) -> str:
    """Converte um nome para identificador URI seguro."""
    return re.sub(r'[\s]+', '_', name.strip()).replace("(", "").replace(")", "")

g = Graph()
g.parse("medical.ttl", format="turtle")
g.bind("", EX)

print("\nA processar Disease_Syntoms.csv...")
doenças_vistas = set()

with open("Disease_Syntoms.csv", newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        disease_name = row["Disease"].strip()
        disease_uri  = EX[uri_safe(disease_name)]

        # criar instância de doença (uma só vez por nome)
        if disease_uri not in doenças_vistas:
            doenças_vistas.add(disease_uri)
            if (disease_uri, RDF.type, EX.Disease) not in g:
                g.add((disease_uri, RDF.type, EX.Disease))
                g.add((disease_uri, EX.name, Literal(disease_name)))

        # sintomas das colunas Symptom_1 … Symptom_17
        for col in reader.fieldnames[1:]:
            sym_raw = row.get(col, "").strip()
            if not sym_raw:
                continue
            sym_uri = EX[uri_safe(sym_raw)]

            if (sym_uri, RDF.type, EX.Symptom) not in g:
                g.add((sym_uri, RDF.type, EX.Symptom))
                g.add((sym_uri, EX.name, Literal(sym_raw)))

            g.add((disease_uri, EX.hasSymptom, sym_uri))

# ── Disease_Description.csv ──────────────────────────────────────────────────
print("A processar Disease_Description.csv...")
with open("Disease_Description.csv", newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        disease_name = row["Disease"].strip()
        description  = row["Description"].strip()
        disease_uri  = EX[uri_safe(disease_name)]

        # garantir que a doença existe
        if (disease_uri, RDF.type, EX.Disease) not in g:
            g.add((disease_uri, RDF.type, EX.Disease))
            g.add((disease_uri, EX.name, Literal(disease_name)))

        g.add((disease_uri, EX.description, Literal(description)))

# ── gravar checkpoint 1 ──────────────────────────────────────────────────────
g.serialize(destination="med_doencas.ttl", format="turtle")
print(f"\n✓ Gravado: med_doencas.ttl  ({len(g)} triplos)")

# ── Disease_Treatment.csv ────────────────────────────────────────────────────
print("\nA processar Disease_Treatment.csv...")
with open("Disease_Treatment.csv", newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        disease_name = row["Disease"].strip()
        disease_uri  = EX[uri_safe(disease_name)]

        if (disease_uri, RDF.type, EX.Disease) not in g:
            g.add((disease_uri, RDF.type, EX.Disease))
            g.add((disease_uri, EX.name, Literal(disease_name)))

        # tratamentos nas colunas Precaution_1 … Precaution_4
        for col in reader.fieldnames[1:]:
            trt_raw = row.get(col, "").strip()
            if not trt_raw:
                continue
            trt_uri = EX[uri_safe(trt_raw)]

            if (trt_uri, RDF.type, EX.Treatment) not in g:
                g.add((trt_uri, RDF.type, EX.Treatment))
                g.add((trt_uri, EX.name, Literal(trt_raw)))

            g.add((disease_uri, EX.hasTreatment, trt_uri))

# ── gravar checkpoint 2 ──────────────────────────────────────────────────────
g.serialize(destination="med_tratamentos.ttl", format="turtle")
print(f"✓ Gravado: med_tratamentos.ttl  ({len(g)} triplos)")