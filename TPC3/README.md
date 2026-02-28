# Resumo
Este trabalho incidiu sobre a tecnologia de base de dados GraphDB e a linguagem SPARQL.

## Resultados
### 1. Manifesto
### 1.1. Alterações à Ontologia

- Movida classe `PratoComPolvo` de `owl:Thing` para `PratoCarnívoro`.
- Removido indivíduo `PolvoIngrediente`.
- Substituída propriedade `:temIngrediente PolvoIngrediente` por `:temIngrediente IngredientePolvo` no indivíduo `EnsopadoCanibal`.
- Removido do indivíduo `Aristóteles` as propriedades `come EnsopadoCanibal` e `come PratoDoDia` pois ambos os pratos contém Polvo como ingrediente
e como o indivíduo `Aristóteles` é um polvo ao comer estes pratos geraria uma inconsistência.
- A classe `RoboCozinheiro` é subclasse tanto de `Máquina` quanto de `Cozinheiro` (que é subclasse de `Funcionário`, subclasse de `Pessoa`), ou seja, gera uma inconsistência pois um robo será simultaneamente uma máquina e uma pessoa.

### 2. Queries SPARQL
### 2.1. Quem foram os clientes?
Query:

Resposta:

### 2.2. Que pratos serve o restaurante?
Query:

Resposta:

### 2.3. Quais os ingredientes necessários á confecção dos pratos (todos)?
Query:

Resposta:

### 2.4. Há funcionários que sejam também clientes?
Query:

Resposta:
