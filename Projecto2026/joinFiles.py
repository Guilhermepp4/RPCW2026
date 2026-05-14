import re

with open("Ontologias/ensino.ttl", encoding="utf-8") as f:
    ensino = f.read()

with open("Ontologias/finalmonumentosPT.ttl", encoding="utf-8") as f:
    mon = f.read()

# remove prefixes e ontology do segundo
mon = re.sub(r'@prefix.*?\n', '', mon)
mon = re.sub(r'@base.*?\n', '', mon)
mon = re.sub(r'<http://.*?owl:Ontology \.\n', '', mon)

final = ensino + "\n\n" + mon

with open("Ontologias/turismoPT.ttl", "w", encoding="utf-8") as f:
    f.write(final)
