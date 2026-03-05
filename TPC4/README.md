# Resumo
Este trabalho consistiu na criação, povoamento e exploração de uma ontologia relativa a uma biblioteca temporal, utilizando tecnologias da Web Semântica.

## Resultados
### 1. Manifesto
### 1.1. Modelar a Ontologia
A primeira parte do tpc consistiu em modelar a ontologia utilizando a ferramenta **Protégé**, resultando no ficheiro [`biblioteca_Temporal.ttl`](https://github.com/Guilhermepp4/RPCW2026/tree/main/TPC4/biblioteca_Temporal.ttl)

### 1.2. Povoamento da ontologia
Em seguida foi disponibilizado dois ficheiros [`dataset_temporal_100.json`](https://github.com/Guilhermepp4/RPCW2026/tree/main/TPC4/dataset_temporal_100.json) e [`dataset_temporal_v2_100.json`](https://github.com/Guilhermepp4/RPCW2026/tree/main/TPC4/dataset_temporal_v2_100.josn) com o objetivo de povoar a ontologia previamente criada.
### 1.2.1 Povoamento
Para o Povoamento da ontologia foi desenvolvido um script em Python [`importInfo.py`](https://github.com/Guilhermepp4/RPCW2026/tree/main/TPC4/importInfo.py) que criou automaticamente indivíduos das classes definidas na ontologia e estabeleceu as relações entre os novos indivíduos.

### 2. Queries SPARQL
### 2.1. Quem foram os clientes?
Query:
```sparql

```
Resposta:
```
```
### 2.2. Que pratos serve o restaurante?
Query:
```sparql

```
Resposta:
```
```
### 2.3. Quais os ingredientes necessários á confecção dos pratos (todos)?
Query:
```sparql
```
Resposta:

### 2.4. Há funcionários que sejam também clientes?
Query:
```sparql
```
Resposta:
```
```

