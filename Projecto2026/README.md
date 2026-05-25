# 🇵🇹 Portugal Semântico: Plataforma de Exploração e Coesão do Património Nacional

## 🎓 Enquadramento Académico
* **Instituição:** Universidade do Minho (UMinho)
* **Unidade Curricular:** Representação e Processamento de Conhecimento na Web (RPCW)
* **Autor:** Guilherme Pinto Pinho
* **Número de Aluno:** PG60263
* **Ano Letivo:** 2025/2026

---

## 📝 Descrição Geral do Projeto
O projeto **Portugal Semântico** é uma plataforma Web completa assente em **Tecnologias da Web Semântica** que visa extrair, modelar, interligar e disponibilizar conhecimento estruturado sobre o património português. O sistema cobre a grande maioria dos monumentos históricos de Portugal Continental e dos Arquipélagos das Regiões Autónomas (Açores e Madeira).

Ao contrário das aplicações Web tradicionais baseadas em bases de dados relacionais (SQL), este ecossistema utiliza um **Grafo de Conhecimento** armazenado em formato RDF/Turtle (`.ttl`). Toda a navegação, filtragem georreferenciada e pesquisa da plataforma são resolvidas através de consultas estruturadas **SPARQL**, demonstrando o potencial da inferência de dados e da criação de recursos únicos na Web.

---

## 📂 Arquitetura e Estrutura do Repositório

O projeto encontra-se organizado na seguinte árvore de diretorias:

```text
├── datasets_finished/
│   ├── monumentos.json                # Dados extraídos de Portugal Continental
│   ├── monumentosArq.json             # Dados extraídos dos Arquipélagos (Açores e Madeira)
│   └── monumentosDescricao.json       # Enriquecimento de metadados detalhados (Continental)
├── Ontologias/
│   ├── monumentosOriginal.ttl         # TBox e estrutura ontológica inicial base
│   ├── finalmonumentosPt.ttl          # Grafo intermédio pós-triplificação da 1ª fase
│   └── finalmonumentosPt_atualizada.ttl # ABOX FINAL: Grafo totalmente enriquecido com descrições
├── src/
│   ├── scrapingM.py                   # Extrator inicial (Monumentos do Continente)
│   ├── scrapingMI.py                  # Extrator inicial (Monumentos das Ilhas)
│   ├── scrapingM2.py                  # Extrator profundo (História e Coordenadas no Continente)
│   └── injectData.py                  # Script de conversão JSON -> Triplos RDF (TTL)
├── templates/
│   ├── starrt.html                    # Dashboard principal (Mapa, Filtros e Listagens)
│   ├── monumento.html                 # Vista atómica de detalhes por instância/URI
│   └── addMonumento.html              # Interface de inserção de novas instâncias para a Ontologia
├── app.py                             # Controlador central da aplicação em Flask
└── mquery.py                          # Módulo de abstração de Queries SPARQL nativas
```

## 🔄 Fluxo de Desenvolvimento (Pipeline de Dados)

### Fase 1: Extração e Mapeamento Inicial (Scraping)
[`scrapingM.py`](https://github.com/Guilhermepp4/RPCW2026/blob/main/Projecto2026/src/scrapingM.py): Efetuou a extração automatizada de dados básicos dos monumentos localizados em Portugal Continental.
[`scrapingMI.py`](https://github.com/Guilhermepp4/RPCW2026/blob/main/Projecto2026/src/scrapingMI.py): Executou em paralelo o levantamento focado nos monumentos dos arquipélagos da Madeira e dos Açores.
Os resultados foram estruturados em ficheiros .json independentes dentro da pasta [`datasets_finished`](https://github.com/Guilhermepp4/RPCW2026/tree/main/Projecto2026/datasets_finished).

### Fase 2: Enriquecimento de Dados
[`scrapingM2.py`](https://github.com/Guilhermepp4/RPCW2026/blob/main/Projecto2026/src/scrapingM2.py): Realizou um scraping secundário com o objetivo de obter mais informações (sub-nomes descrições). Esta informação estruturada foi compilada em [`monumentosDescricao.json`](https://github.com/Guilhermepp4/RPCW2026/blob/main/Projecto2026/datasets_finished/monumentosDescricao.json). (Nota: Estes metadados detalhados apenas se encontravam disponíveis para Portugal Continental).

### Fase 3: Triplificação e Modelagem Semântica
Através do script de tratamento e injeção de dados ([`injectData.py`](https://github.com/Guilhermepp4/RPCW2026/blob/main/Projecto2026/src/injectData.py) / [`tratarMonumentos.py`]((https://github.com/Guilhermepp4/RPCW2026/blob/main/Projecto2026/src/tratarMonumentos.py))), a informação crua guardada em JSON foi processada, convertida em triplos RDF de acordo com o esquema da ontologia e guardada em formato Turtle (.ttl) dentro da pasta [`Ontologias/`](https://github.com/Guilhermepp4/RPCW2026/tree/main/Projecto2026/Ontologias). O resultado final consolidado está refletido no ficheiro [`finalmonumentosPt_atualizada.ttl`](https://github.com/Guilhermepp4/RPCW2026/blob/main/Projecto2026/Ontologias/finalmonumentosPT_atualizada.ttl).

### Fase 4: Desenvolvimento da Aplicação Web
[`mquery.py`](https://github.com/Guilhermepp4/RPCW2026/blob/main/Projecto2026/mquery.py): Centraliza a lógica de comunicação SPARQL.

[`app.py`](https://github.com/Guilhermepp4/RPCW2026/blob/main/Projecto2026/app.py): Servidor Flask que escuta os pedidos do utilizador, interage com o [`mquery.py`](https://github.com/Guilhermepp4/RPCW2026/blob/main/Projecto2026/mquery.py) para obter os dados em formato semântico, e renderiza as páginas do frontend localizadas em [`templates/`](https://github.com/Guilhermepp4/RPCW2026/tree/main/Projecto2026/templates).

### 🔥 Funcionalidades Principais do Website

- Exploração Interativa: Mapa dinâmico para localização visual e geográfica do património nacional.

- Filtros Avançados: Segmentação eficaz de monumentos por Regiões e por Tipo de Monumento (ex: Estruturas
Militares, Edifícios Religiosos, Monumentos Civis, etc).

- Painel Independente de Favoritos: Zona fixa gerida via que permite guardar monumentos para consulta futura.

- Escrita de Conhecimento: Permite aos utilizadores enriquecer a base de dados em tempo real através do formulário de submissão, mantendo a ontologia em constante evolução.

### 🛠️ Stack Tecnológica

- Modelagem Semântica: Protégé, RDF, Turtle (.ttl), SPARQL.

- Backend: Python, Flask.

- Frontend: HTML, JavaScript, CSS, W3.CSS.