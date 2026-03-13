# Resumo
Este trabalho consistiu na criação, povoamento e exploração de uma ontologia relativa a uma biblioteca temporal, utilizando tecnologias da Web Semântica.

## Resultados
### 1. Manifesto
### 1.1. Modelar a Ontologia
A primeira parte do tpc consistiu em modelar a ontologia utilizando a ferramenta **Protégé**, resultando no ficheiro [`biblioteca_Temporal.ttl`](https://github.com/Guilhermepp4/RPCW2026/tree/main/TPC4/files/biblioteca_Temporal.ttl)

### 1.2. Povoamento da ontologia
Após a criação da ontologia base, foi desenvolvido um script em Python[`importarInfo.py`](https://github.com/Guilhermepp4/RPCW2026/tree/main/TPC4/importarInfo.py) com o objetivo de popular automaticamente a ontologia com indivíduos presentes nos datasets fornecidos [`dataset_temporal_100.json`](https://github.com/Guilhermepp4/RPCW2026/tree/main/TPC4/datasets/dataset_temporal_100.json) e [`dataset_temporal_v2_100`](https://github.com/Guilhermepp4/RPCW2026/tree/main/TPC4/datasets/dataset_temporal_v2_100.json).

Para este efeito foi utilizada a biblioteca **rdflib**, que permite manipular grafos RDF de forma programática. O script começa por carregar a ontologia base a partir do ficheiro [`biblioeca_Temporal.ttl`](https://github.com/Guilhermepp4/RPCW2026/tree/main/TPC4/files/biblioteca_Temporal.ttl), utilizando o formato Turtle. De seguida é definido o namespace da ontologia, que é utilizado para criar os URIs dos indivíduos e propriedades.

O script percorre todos os objetos presentes nestes datasets e cria os respetivos indivíduos no grafo RDF.

Para cada elemento do dataset são realizadas as seguintes operações:

- Criação do indivíduo com base no identificador (id) presente no dataset.

- Associação da classe correspondente ao tipo (tipo) através da propriedade rdf:type.

- Adição de propriedades literais, como o nome do indivíduo.

- Adição de propriedades de objeto que ligam os indivíduos entre si, como:

  - trabalhaEm

  - escritoPor

  - pertenceA

  - refere

  - existeEm

Adicionalmente, o script trata propriedades que podem ter múltiplos valores, como existeEm, verificando se o valor é uma lista e adicionando todas as relações necessárias ao grafo.
Após o processamento dos datasets, o grafo RDF resultante é serializado e guardado num novo ficheiro Turtle [`biblioteca_Temporal_Final.ttl`](https://github.com/Guilhermepp4/RPCW2026/tree/main/TPC4/files/biblioteca_Temporal_Final.ttl), contendo a ontologia já povoada com os indivíduos.

### 1.3. Limitações

Durante o desenvolvimento do trabalho foram identificadas algumas limitações relacionadas principalmente com a estrutura e conteúdo dos datasets fornecidos.
Uma das limitações encontradas foi a ausência de indivíduos pertencentes diretamente à classe Livro nos datasets utilizados. Em vez disso, os dados apenas contêm indivíduos de subclasses específicas, como por exemplo LivroHistorico. Esta situação impossibilita testar diretamente consultas ou restrições que dependam explicitamente da existência de indivíduos da classe genérica Livro.
Adicionalmente, algumas das condições definidas no enunciado envolvem relações complexas entre diferentes entidades e contextos temporais. De forma a garantir que as queries SPARQL funcionassem corretamente com os dados disponíveis, foi necessário simplificar ou remover algumas condições nas consultas, mantendo apenas os critérios essenciais para a obtenção dos resultados pretendidos.
Estas decisões permitiram garantir a correta execução das queries e a coerência dos resultados obtidos, embora algumas restrições mais específicas não possam ser completamente verificadas com os dados disponíveis.

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

### 2.8. Liste todos os livros que existem em pelo menos uma linha temporal alternativa (LinhaAlternativa)
Query:
```sparql
SELECT ?livro WHERE {
    ?linha a :LinhaAlternativa .
    ?livro :existeEm ?linha .
}
```

### 2.9. Indique todos os bibliotecários e a biblioteca onde trabalham
Query:
```sparql
SELECT ?pessoa ?biblioteca WHERE {
    ?pessoa a :Bibliotecário ;
    		:trabalhaEm ?biblioteca .
}
```

### 2.10. Liste todos os livros escritos por Cronos e indique em que linhas temporais esses livros existem
Query:
```sparql
SELECT ?livro ?linha WHERE {
    ?livro :escritoPor :Cronos ;
    		:existeEm ?linha .
    ?linha a :LinhaTemporal .
}

```

### 2.11. Identifique livros que não referem nenhum evento
Query:
```sparql
SELECT ?livro (count(?evento) as ?numEvento)WHERE {
    Optional {?livro :refereEvento ?evento }
} group by ?livro
having (?numEvento = 0)
```

### 2.12. Verifique se existe algum livro sem linha temporal associada
Query:
```sparql
SELECT ?livro (count(?linha) as ?numEvento)WHERE {
    ?linha a :LinhaTemporal .
    Optional {?livro :existeEm ?linha }
} group by ?livro
having (?numEvento = 0)
```

### 2.13. Identifique autores que sejam também leitores (caso essa propriedade esteja modelada)
Query:
```sparql
SELECT ?pessoa WHERE {
    ?pessoa a :Autor ;
            a :Leitor .
}
```
