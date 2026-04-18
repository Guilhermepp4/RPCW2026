import tabula
import pandas as pd

lista_tabelas = tabula.read_pdf("datasets/ListaPresidentesCM.pdf", pages='all')

# 2. Juntar tudo num único DataFrame do Pandas
df = pd.concat(lista_tabelas)


# 4. Guardar em JSON
df.to_json("presidentes_camara.json", orient="records", indent=4, force_ascii=False)