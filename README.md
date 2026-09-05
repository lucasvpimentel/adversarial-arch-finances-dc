# 🏛️ Comitê de Investimento Multi-Agente (Adversarial Architecture)

Sistema multi-agente de análise financeira e tomada de decisão sobre ativos de mercado (B3 e EUA), desenvolvido em **Python** utilizando **LangGraph**, **LangChain**, **OpenAI**, **yfinance** e **DuckDuckGo Search**.

O projeto adota uma **arquitetura adversarial (dialética)** onde dois analistas de IA com perspectivas opostas (um otimista/Bull e um cético/Bear) debatem com base em dados reais de mercado e notícias antes que um Gestor imparcial emita o veredito final de investimento.

---

## 🔬 Teoria Básica e Fundamentos Arquiteturais

### 1. Dialética Adversarial Multi-Agente (Bull vs. Bear)
Modelos de Linguagem (LLMs) executados individualmente costumam sofrer de **viés de confirmação** e tomadas de decisão unilateral. Para mitigar esse problema, o sistema aplica o método dialético:
- **Nó Coletor (Fonte Única da Verdade)**: Busca dados quantitativos reais (últimos 30 dias via `yfinance`) e dados qualitativos (notícias recentes da web). Ambos os analistas recebem **exatamente o mesmo contexto inicial**, garantindo simetria de informação.
- **Agente Bull (Tese)**: Forçado pelo prompt de sistema a extrair os catalisadores positivos, métricas de crescimento e potencial do ativo.
- **Agente Bear (Antítese)**: Forçado pelo prompt de sistema a identificar riscos, volatilidade, valuation esticado e incertezas.
- **Rodada de Réplicas (Aprofundamento)**: Cada analista recebe a tese inicial do adversário e rebate os pontos divergentes, testando a solidez dos argumentos opostos.
- **Gestor / Juiz (Síntese)**: Um árbitro neutro analisa o debate completo (argumentos iniciais + réplicas) e decide entre **COMPRAR**, **AGUARDAR** ou **EVITAR**, atribuindo um nível de confiança (Baixo, Médio ou Alto).

### 2. Paradigma Estritamente Funcional / Procedural
Todo o código do projeto foi construído **sem Orientação a Objetos (OOP)**:
- Sem classes de comportamento, sem herança e sem encapsulamento com métodos personalizados.
- As definições de Estado no LangGraph utilizam a sintaxe funcional do `TypedDict` (`TypedDict("EstadoComite", {...})`).
- Cada nó do grafo é uma **função pura** (`def no_exemplo(estado: EstadoComite) -> dict:`) que aceita o estado compartilhado e retorna um dicionário contendo **apenas as chaves atualizadas**.

### 3. Concorrência e Sincronização em Grafos (LangGraph)

```text
[START] -> coletor_dados -> (FAN-OUT 1) -> [agente_bull] --\
                                        -> [agente_bear] ---+-> (BARREIRA DE SINCRONIZAÇÃO)
                                                                  |
                                        /-------------------------/
                                        |
                                        +-> (FAN-OUT 2) -> [replica_bull] --\
                                                        -> [replica_bear] ---+-> (FAN-IN 2) -> gestor_juiz -> [END]
```

- **Fan-Out 1 (Execução Paralela Iniciais)**: O nó `coletor_dados` dispara simultaneamente `agente_bull` e `agente_bear`. Como ambos necessitam apenas dos dados de mercado, rodam de forma concorrente reduzindo a latência pela metade.
- **Barreira de Sincronização Intermediária**: A réplica do Bull depende do argumento inicial do Bear (e vice-versa). As saídas da primeira rodada convergem em um ponto de sincronização, garantindo que as réplicas só iniciem quando ambas as teses iniciais estiverem gravadas no estado.
- **Fan-Out 2 & Fan-In 2**: As réplicas executam em paralelo e convergem para o `gestor_juiz`, que emite a síntese final.

---

## 📁 Estrutura do Projeto

```text
Multi Agentes/
│
├── .env.example               # Modelo de variáveis de ambiente
├── .gitignore                 # Proteção contra commit de chaves sensíveis
├── requirements.txt           # Dependências do projeto
├── README.md                  # Documentação completa
├── main.py                    # Ponto de entrada interativo (CLI)
│
├── config/
│   ├── __init__.py
│   └── ativos.py              # Lista de 30 ativos (B3 e EUA) e validação de ticker
│
├── estado/
│   ├── __init__.py
│   └── estado.py              # Definicao funcional do EstadoComite (TypedDict)
│
├── nos/
│   ├── __init__.py
│   ├── coletor.py             # Coleta quantitativa (yfinance) e qualitativa (DuckDuckGo)
│   ├── agente_bull.py         # Nó do Analista Otimista
│   ├── agente_bear.py         # Nó do Analista Cético
│   ├── replica_bull.py        # Nó de Réplica Otimista
│   ├── replica_bear.py        # Nó de Réplica Cética
│   └── gestor_juiz.py         # Nó do Gestor / Juiz Decisor
│
├── grafo/
│   ├── __init__.py
│   └── grafo.py               # Montagem declarativa do StateGraph com Fan-Out e Fan-In
│
└── prompts/                   # Arquivos Markdown com os prompts de sistema
    ├── agente_bull.md
    ├── agente_bear.md
    ├── replica_bull.md
    ├── replica_bear.md
    └── gestor_juiz.md
```

---

## 🚀 Como Configurar e Executar

### 1. Pré-requisitos
- Python 3.10 ou superior
- Chave de API da OpenAI (`OPENAI_API_KEY`)

### 2. Instalação das Dependências

```bash
python -m pip install -r requirements.txt
```

### 3. Configuração do Arquivo `.env`

Crie um arquivo `.env` na raiz do projeto com base no `.env.example`:

```env
OPENAI_API_KEY=sk-sua-chave-openai-aqui
OPENAI_MODEL=gpt-4o-mini
TEMPERATURE=0.2
```

### 4. Executando o Sistema

Para iniciar a interface interativa de linha de comando:

```bash
python main.py
```

---

## 📈 Exemplo de Relatório Gerado

Ao selecionar um ticker (ex: `TSLA` ou `PETR4.SA`), o terminal exibirá todo o debate em tempo real:

1. **📊 Dados de Mercado**: Cotação inicial/final dos últimos 30 dias, variação %, volume médio e notícias recentes.
2. **🐂 Tese Inicial Bull**: Argumentos a favor da compra baseados estritamente nos dados.
3. **🐻 Tese Inicial Bear**: Alertas de risco, valuation e incertezas.
4. **🔄 Réplica Bull**: Desconstrução dos riscos apontados pelo Bear.
5. **🔄 Réplica Bear**: Desconstrução do otimismo apontado pelo Bull.
6. **👨‍⚖️ Relatório e Decisão do Gestor**: Recomendação final (`COMPRAR`, `AGUARDAR` ou `EVITAR`) com nível de confiança e síntese ponderada.

---

## 🛠️ Tecnologias Utilizadas

- **[LangGraph](https://github.com/langchain-ai/langgraph)**: Orquestração de grafos de estados e fluxos de agentes concorrentes.
- **[LangChain OpenAI](https://github.com/langchain-ai/langchain)**: Integração com os modelos de linguagem da OpenAI.
- **[yfinance](https://github.com/ranaroussi/yfinance)**: Coleta de histórico de preços e volumes de ações.
- **[DuckDuckGo Search](https://github.com/deedy5/ddgs)**: Busca de notícias financeiras recentes na web.
