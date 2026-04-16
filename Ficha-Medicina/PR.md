# PR.md – RPCW2026 Ficha Medicina 🧬

## 📌 Introdução

No âmbito da ficha **RPCW2026 – Medicina**, foi desenvolvida uma solução completa para:

* Modelação e extensão de uma ontologia no domínio da medicina
* Povoamento automático da ontologia com dados reais (CSV e JSON)
* Execução de queries SPARQL para análise e transformação de dados
* Integração com GraphDB

---

## 🧱 Estrutura da Solução

A solução foi dividida em três etapas principais:

1. **Povoamento inicial com dados CSV**
2. **Extensão com dados de doentes (JSON)**
3. **Importação para GraphDB e execução de queries**

---

## ⚙️ Scripts Desenvolvidos

### 1️⃣ `import_csv.py` – Povoamento com doenças

Este script é responsável por criar a base da ontologia a partir de ficheiros CSV.

### 📥 Inputs:

* `medical.ttl` (ontologia base)
* `Disease_Syntoms.csv`
* `Disease_Description.csv`
* `Disease_Treatment.csv`

### 📤 Outputs:

* `med_doencas.ttl`
* `med_tratamentos.ttl`

### 🔍 Funcionalidades:

* Criação de instâncias da classe `:Disease`
* Criação de `:Symptom` e associação via `:hasSymptom`
* Adição de descrições (`:description`)
* Criação de `:Treatment` e associação via `:hasTreatment`
* Normalização de URIs com função `uri_safe`

---

### 2️⃣ `import_json.py` – Povoamento com doentes

Este script adiciona instâncias da classe `:Patient` com base num ficheiro JSON.

### 📥 Inputs:

* `med_tratamentos.ttl`
* `doentes.json`

### 📤 Output:

* `med_doentes.ttl`

### 🔍 Funcionalidades:

* Criação de indivíduos `:Patient`
* Associação de sintomas com `:exhibitsSymptom`
* Reutilização de sintomas existentes na ontologia
* Criação dinâmica de novos sintomas caso não existam

---

### 3️⃣ `export.py` – Upload para GraphDB

Script responsável por carregar os dados RDF para o GraphDB via API REST.

### 📥 Input:

* Ficheiro `.ttl`

### ⚙️ Parâmetros:

* `--repo` → nome do repositório (default: Medicina)
* `--url` → endpoint do GraphDB

### ▶️ Exemplo de execução:

```bash
python export.py Ontologias/med_doentes.ttl --repo Medicina
```

### 🔍 Funcionalidades:

* Leitura de ficheiros Turtle
* Envio via HTTP POST para GraphDB
* Tratamento de erros e feedback ao utilizador

---

## ▶️ Como Reproduzir

### 1. Preparação

* Garantir que o GraphDB está ativo:

  ```
  http://localhost:7200
  ```
* Criar um repositório chamado `Medicina`

---

### 2. Executar os scripts

#### Passo 1 – Povoar com doenças

```bash
python import_csv.py
```

#### Passo 2 – Adicionar doentes

```bash
python import_json.py
```

#### Passo 3 – Carregar no GraphDB

```bash
python export.py Ontologias/med_doentes.ttl --repo Medicina
```

---

## 🔎 Queries SPARQL

Foram desenvolvidas queries para exploração dos dados.
Ver Ficheiro [`sparql.txt`](https://github.com/Guilhermepp4/RPCW2026/blob/main/Ficha-Medicina/sparql.txt)

---

## 📅 Data

23 de Março de 2026

## 📝 Autor

Guilherme Pinto Pinho pg60263
