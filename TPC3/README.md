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
```sparql
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  
PREFIX owl: <http://www.w3.org/2002/07/owl#>  
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>  
PREFIX : <http://example.org/polvo-filosofico#>  
SELECT ?Cliente WHERE {  
    ?Cliente a :Cliente .  
} 
```
Resposta:
```
1:Ana
2:Bruno
3:Carla
4:Daniel
5:Eva
6:Schrodinger
```
### 2.2. Que pratos serve o restaurante?
Query:
```sparql
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  
PREFIX owl: <http://www.w3.org/2002/07/owl#>  
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>  
PREFIX : <http://example.org/polvo-filosofico#>  
SELECT ?Prato WHERE {  
    ?Prato a :Prato .  
}
```
Resposta:
```
1:SaladaExistencial
2:BifeDeterminista
3:PratoDoObservador
4:EnsopadoCanibal
5:DilemaDoSer
6:PratoDoDia
7:PeixeDoLivreArbitrio
8:TofuMetafisico
```
### 2.3. Quais os ingredientes necessários á confecção dos pratos (todos)?
Query:
```sparql
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  
PREFIX owl: <http://www.w3.org/2002/07/owl#>  
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>  
PREFIX : <http://example.org/polvo-filosofico#>  
SELECT ?Prato (GROUP_CONCAT(STRAFTER(STR(?Ingrediente), "#"); separator=", ") AS ?Ingredientes) WHERE {  
    ?Prato a :Prato;
        :temIngrediente ?Ingrediente .
}  Group by ?Prato
```
Resposta:
| Prato  | Ingredientes          |
|--------|----------------------|
| SaladaExistencial  | Alface, Tomate       |
| BifeDeterminista   | CarneVaca                 |
| PratoDoObservador  | Cogumelos, Peixe       |
| EnsopadoCanibal   | IngredientePolvo                 |
| DilemaDoSer  | CarneVaca, Tofu       |
| PratoDoDia   | IngredientePolvo                 |
| PeixeDoLivreArbitrio  | Peixe       |
| TofuMetafisico   | Cogumelos, Tofu                 |

### 2.4. Há funcionários que sejam também clientes?
Query:
```sparql
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  
PREFIX owl: <http://www.w3.org/2002/07/owl#>  
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>  
PREFIX : <http://example.org/polvo-filosofico#>  
SELECT ?Pessoa WHERE {
    ?Pessoa a :Cliente;
    			 a :Funcionario .
}  
```
Resposta:

```
1:Schrodinger
```

