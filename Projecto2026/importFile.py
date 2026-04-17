import requests, argparse, os

def upload_to_graphdb(endpoint, repoID, file):
    if not os.path.exists(file):
        print(f"Erro: O ficheiro '{file} não foi encontrado...")
    else:
        url = f"{endpoint}/repositories/{repoID}/statements"
        headers = {"Content-Type": "text/turtle;charset=utf-8"}
        print(f"A ler o ficheiro '{file}'...")
        try:
            with open(file, encoding="UTF-8") as f:
                ttl = f.read()
            print(f"A carregar os dados no repositorio '{repoID}'...")
            response = requests.post(url, data=ttl, headers=headers)
            if response.status_code in [200, 201, 204]:
                print("Dataset carregado com sucesso!")
            else:
                print(f"Erro ao carregar a informação: {response.status_code}.")
                print(response.text)
        except Exception as e:
            print(f"Ocoreu um erro inesperado: {e}.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Carregar um dataset Turtle (.ttl) no GraphDB")
    parser.add_argument("ficheiro", help="")
    parser.add_argument("--repo", default="FestivaisEventos", help="ID do repositório no GraphDB")
    parser.add_argument("--url", default="http://localhost:7200", help="URL do GraphDB (default: http://localhost:7200) ")

    args = parser.parse_args()
    upload_to_graphdb(args.url, args.repo, args.ficheiro)