# TPC6 - Representação e Processamento de Conhecimento na Web

## 📚 Descrição

Este trabalho foi desenvolvido no âmbito da unidade curricular **Representação e Processamento de Conhecimento na Web (RPCW)**.

O objetivo deste TPC foi desenvolver uma **aplicação web em Python utilizando Flask** que interage com uma **base de conhecimento RDF armazenada no GraphDB**, permitindo consultar informação sobre **linhas temporais e livros associados** através de **queries SPARQL**.

A aplicação permite:

* Listar todas as **linhas temporais**
* Visualizar os **detalhes de uma linha temporal**
* Consultar os **livros existentes em cada linha temporal**

---
# ⚙️ Funcionamento da aplicação

A aplicação comunica com o **GraphDB** através de **queries SPARQL**.
Os resultados são recebidos em formato **JSON**, processados em Python e enviados para os **templates Jinja2** para renderização das páginas HTML.

---

# 🔎 Rotas da aplicação

## 1️⃣ Listar Linhas Temporais

```
/linhas
```

Esta rota executa a seguinte query SPARQL:

```sparql
PREFIX : <http://example.org/biblioteca-temporal#>

SELECT ?linhaID ?LinhaTipo WHERE {
    ?linha a ?tipoLinha .
    FILTER(?tipoLinha IN (:LinhaOriginal, :LinhaAlternativa))

    BIND(STRAFTER(STR(?linha), '#') AS ?linhaID)
    BIND(STRAFTER(STR(?tipoLinha), '#') AS ?LinhaTipo)
}
```

### Objetivo

Obter todas as **linhas temporais existentes** na base de conhecimento.

### Informação apresentada

* Identificador da linha temporal
* Tipo de linha temporal

### Interface

Os resultados são apresentados numa **tabela HTML**, onde cada linha temporal possui um **link para a página de detalhe**.

---

## 2️⃣ Detalhe de uma Linha Temporal

```
/linha/<linhaID>
```

Esta rota permite consultar **todos os livros existentes numa linha temporal específica**.

### Query SPARQL utilizada

```sparql
PREFIX : <http://example.org/biblioteca-temporal#>

SELECT ?LinhaTipo 
       (GROUP_CONCAT(?livros; separator=",") AS ?Livros)
       (GROUP_CONCAT(?titulo; separator="|") AS ?Titulo)
       (GROUP_CONCAT(?tipo_Livro; separator=", ") AS ?LivroTipo)
WHERE {

    :<linhaID> a ?tipoLinha .

    ?livro :existeEm :<linhaID> ;
           :titulo ?titulo ;
           a ?tipoLivro .

    FILTER(?tipoLinha IN (:LinhaOriginal, :LinhaAlternativa))
    FILTER(?tipoLivro IN (:LivroParadoxal, :LivroHistorico, :LivroFiccional))

    BIND(STRAFTER(STR(?livro), '#') AS ?livros)
    BIND(STRAFTER(STR(?tipoLinha), '#') AS ?LinhaTipo)
    BIND(STRAFTER(STR(?tipoLivro), '#') AS ?tipo_Livro)

}
GROUP BY ?LinhaTipo
```

### Objetivo

Obter todos os **livros que existem numa linha temporal específica**.

### Informação apresentada

Para cada livro:

* ID do livro
* Título
* Tipo de livro

---

# 🧩 Processamento dos resultados

Os resultados da query são recebidos em **JSON** e depois processados em Python.

Como os livros são obtidos com `GROUP_CONCAT`, os valores são separados usando:

```python
split(",")
split("|")
```

Posteriormente, os dados são organizados numa estrutura de dicionário:

```python
line = {
    "Linha_T0": {
        "Linha_Id": "...",
        "Tipo_de_Linha": "...",
        "Livros_Existentes": {
            "Livro1": {...},
            "Livro2": {...}
        }
    }
}
```

# 🎨 Interface Web

A interface foi construída com:

* **HTML**
* **Jinja2**
* **W3.CSS**

### Página de linhas temporais

Apresenta uma tabela com:

| Linha ID | Tipo da Linha |
| -------- | ------------- |

Cada linha possui um **link clicável** que redireciona para a página de detalhe.

---

### Página de detalhe da linha

Apresenta uma tabela com:

| Linha ID | Tipo da Linha | Livro | Título | Tipo de Livro |
| -------- | ------------- | ----- | ------ | ------------- |

Cada livro possui um **link para a página individual do livro**.

---

# ▶️ Como executar a aplicação

### 1️⃣ Instalar dependências

```bash
pip install flask requests
```

---

### 2️⃣ Iniciar o GraphDB

Certificar que o **GraphDB está a correr** em:

```
http://localhost:7200
```

---

### 3️⃣ Executar a aplicação

```bash
python app.py
```

---

### 4️⃣ Abrir no browser

```
http://localhost:5000/linhas
```

---

# 📌 Conclusão

Este trabalho permitiu aplicar conceitos importantes da **Web Semântica**, incluindo:

* Modelação de conhecimento em **RDF**
* Consultas **SPARQL**
* Integração de **bases de conhecimento com aplicações web**
* Utilização de **Flask e Jinja2** para criação de interfaces dinâmicas

A aplicação demonstra como é possível **consultar e apresentar conhecimento estruturado na web** de forma interativa.