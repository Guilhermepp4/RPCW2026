import re
import json

def extract(file_path, final_path, tipo):
    res = []
    distrito = None
    with open(file_path, encoding="utf-8") as f:

        for linha in f:
            linha = linha.strip()

            if not linha:
                continue
            
            if tipo == "camara_municipal":
                if "Município" in linha:
                    continue
                
                if linha.startswith("DISTRITO DE"):
                    distrito = linha.replace("DISTRITO DE", "").strip()
                    continue

                if linha.startswith("Região Autónoma dos"):
                    distrito = linha.replace("Região Autónoma dos", "").strip()
                    continue

                if linha.startswith("Região Autónoma da"):
                    distrito = linha.replace("Região Autónoma da", "").strip()
                    continue

                # dividir por 2 ou mais espaços
                partes = re.split(r'\s{2,}', linha)

                if len(partes) >= 3:
                    concelho = partes[0].strip()
                    presidente = partes[1].strip()
                    partido = partes[2].strip()
                    presidente = presidente if presidente != "-" else "Desconhecido"
                    partido = partido if partido != "-" else "Desconecido"

                    res.append({
                        "Distrito": distrito,
                        "Concelho": concelho,
                        "Presidente": presidente,
                        "Partido": partido
                    })
                    
            elif tipo == "freguesias":
                if "Força política" in linha:
                    continue
                
                if linha.startswith("DISTRITO DE") or linha.startswith("Região Autónoma"):

                    match = re.match(
                        r'(DISTRITO DE|Região Autónoma dos|Região Autónoma da)\s+(.*?)\s+Concelho de\s+(.*)',
                        linha
                    )

                    if match:
                        distrito = match.group(2).strip()
                        concelho = match.group(3).strip()
                    continue

                # dividir por 2 ou mais espaços
                partes = re.split(r'\s{2,}', linha)

                if len(partes) >= 3:
                    freguesia = partes[0].strip()
                    presidente = partes[1].strip()
                    partido = partes[2].strip()
                    presidente = presidente if presidente != "-" else "Desconhecido"
                    partido = partido if partido != "-" else "Desconecido"

                    res.append({
                        "Distrito": distrito,
                        "Concelho": concelho,
                        "Freguesia": freguesia,
                        "Presidente": presidente,
                        "Partido": partido
                    })
                if len(partes) < 3:
                    print("LINHA PERDIDA:", linha)

    with open(final_path, "w", encoding="utf-8") as f:
        json.dump(res, f, indent=4, ensure_ascii=False)
    print("Feito!", len(res), "registos")

def main():
    extract("raw_data/outputCM.txt", "datasets/presidentesCM.json", "camara_municipal")
    extract("raw_data/outputJF.txt", "datasets/presidentesJF.json", "freguesias")

if __name__ == "__main__":
    main()