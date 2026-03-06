# Resumo
Este trabalho consistiu na criação, povoamento e exploração de uma ontologia relativa a uma biblioteca temporal, utilizando tecnologias da Web Semântica.

## Resultados
### 1. Manifesto
### 1.1. Modelar a Ontologia
A primeira parte do tpc consistiu em modelar a ontologia utilizando a ferramenta **Protégé**, resultando no ficheiro [`biblioteca_Temporal.ttl`](https://github.com/Guilhermepp4/RPCW2026/tree/main/TPC4/biblioteca_Temporal.ttl)

### 1.2. Povoamento da ontologia
Em seguida foi disponibilizado dois ficheiros [`dataset_temporal_100.json`](https://github.com/Guilhermepp4/RPCW2026/tree/main/TPC4/dataset_temporal_100.json) e [`dataset_temporal_v2_100.json`](https://github.com/Guilhermepp4/RPCW2026/tree/main/TPC4/dataset_temporal_v2_100.josn) com o objetivo de povoar a ontologia previamente criada.
### 1.2.1. Povoamento
Para o Povoamento da ontologia foi desenvolvido um script em Python [`importInfo.py`](https://github.com/Guilhermepp4/RPCW2026/tree/main/TPC4/importInfo.py) que criou automaticamente indivíduos das classes definidas na ontologia e estabeleceu as relações entre os novos indivíduos.

### 2. Queries SPARQL
### 2.1. Liste todos os livros que existem na linha temporal original (LinhaOriginal)
Query:
```sparql
SELECT DISTINCT ?nomeLivro WHERE {
    ?nomeLivro :existeEm ?linhaO .
    ?linhaO a :LinhaOriginal .
} order by ?nomeLivro
```

### 2.2. Identifique os livros que existem em mais do que uma linha temporal
Query:
```sparql
SELECT DISTINCT ?nomeLivro (count(?linhaO) as ?numlinhas) WHERE {
    ?linhaO a :LinhaTemporal .
    ?nomeLivro :existeEm ?linhaO .
} 
group by ?nomeLivro
HAVING (?numlinhas > 1)
ORDER BY DESC(?numLinhas) 
```

### 2.3. Liste todos os livros classificados como LivroParadoxal
Query:
```sparql
SELECT DISTINCT ?livro ?nomeLivro WHERE {
    ?livro a :LivroParadoxal .
    OPTIONAL { ?livro :nome ?nomeLivro } .
}
```

### 2.4. Para cada LivroHistorico, indique os eventos históricos que esse livro refere
Query:
```sparql
SELECT ?livro ?nomeLivro ?evento WHERE {
    ?livro a :LivroHistorico ;
    	   :refereEvento ?evento .
    ?evento a :EventoHistorico .
    OPTIONAL {?livro :nome ?nomeLivro}
}
```

### 2.5. Identifique livros classificados como LivroHistorico que referem eventos futuros
Query:
```sparql
SELECT ?livro ?nomeLivro ?evento WHERE {
    ?livro a :LivroHistorico ;
    	   :refereEvento ?evento .
    ?evento a :EventoFuturo .
    OPTIONAL {?livro :nome ?nomeLivro}
} 
```

### 2.6. Liste os autores e o número de livros que escreveram, ordenando o resultado por número de livros em ordem decrescente
Query:
```sparql
SELECT ?autor ?nomeAutor (count(?livro) as ?numLivro) WHERE {
    ?autor a :Autor .
    ?livro :escritoPor ?autor .
    OPTIONAL {?autor :nome ?nomeAutor}
} GROUP BY ?autor ?nomeAutor
order by desc(?numLivro)
```

### 2.7. Identifique os autores que escreveram pelo menos um livro paradoxal
Query:
```sparql
SELECT ?autor ?nomeAutor WHERE {
    ?autor a :Autor .
    ?livro :escritoPor ?autor .
    ?livro a :LivroParadoxal .
    OPTIONAL {?autor :nome ?nomeAutor}
}
```
Resposta:
```
```

### 2.8. Liste todos os livros que existem em pelo menos uma linha temporal alternativa (LinhaAlternativa)
Query:
```sparql
```
Resposta:
```
```

### 2.9. Indique todos os bibliotecários e a biblioteca onde trabalham
Query:
```sparql
```
Resposta:
```
```

### 2.10. Liste todos os livros escritos por Cronos e indique em que linhas temporais esses livros existem
Query:
```sparql
```
Resposta:
```
```

### 2.11. Identifique livros que não referem nenhum evento
Query:
```sparql
```
Resposta:
```
```

### 2.12. Verifique se existe algum livro sem linha temporal associada
Query:
```sparql
```
Resposta:
```
```

### 2.13. Identifique autores que sejam também leitores (caso essa propriedade esteja modelada)
Query:
```sparql
```
Resposta:
```
```