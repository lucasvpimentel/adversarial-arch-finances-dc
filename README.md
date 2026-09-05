# 🏛️ Comitê de Investimento Multi-Agente (Adversarial Architecture)

Sistema multi-agente de análise financeira e tomada de decisão sobre ativos de mercado (B3 e EUA), desenvolvido em **Python** utilizando **LangGraph**, **LangChain**, **OpenAI**, **yfinance**, **DuckDuckGo Search** e **Streamlit**.

O projeto adota uma **arquitetura adversarial (dialética)** onde analistas de IA com perspectivas opostas (um otimista/Bull e um cético/Bear) debatem com base em dados reais de mercado, estatísticas quantitativas imparciais e notícias, culminando na avaliação simultânea de uma banca com **três Juízes por perfil de risco (Conservador, Moderado e Agressivo)**.

---

## 🔬 Teoria Básica e Fundamentos Arquiteturais

### 1. Dialética Adversarial Multi-Agente (Bull vs. Bear)
Modelos de Linguagem (LLMs) executados individualmente costumam sofrer de **viés de confirmação** e tomadas de decisão unilateral. Para mitigar esse problema, o sistema aplica o método dialético:
- **Nó Coletor & Agente Estatístico (Fontes de Verdade)**: O nó coletor busca dados qualitativos (notícias web) e histórico quantitativo via `yfinance`. O Agente Estatístico calcula métricas puramente matemáticas (volatilidade 30d, variação 7d/30d/90d, SMA-7, SMA-30) de forma imparcial (sem opinião). Todos os agentes recebem exatamente o mesmo contexto inicial.
- **Agente Bull (Tese)**: Extrai os catalisadores positivos, métricas de crescimento e potencial do ativo.
- **Agente Bear (Antítese)**: Identifica riscos, volatilidade, valuation esticado e incertezas.
- **Rodada de Réplicas (Aprofundamento)**: Cada analista recebe a tese inicial do adversário e rebate os pontos divergentes.
- **Banca de 3 Juízes por Perfil de Risco (Síntese)**:
  - 🛡️ **Juiz Conservador**: Prioriza preservação de capital e controle de volatilidade (rigoroso para "Comprar").
  - ⚖️ **Juiz Moderado**: Busca o equilíbrio neutro entre risco e retorno.
  - 🚀 **Juiz Agressivo**: Maximiza potencial de retorno e tolera maior volatilidade.

### 2. Paradigma Estritamente Funcional / Procedural
Todo o código do projeto foi construído **sem Orientação a Objetos (OOP)**:
- Sem classes de comportamento, sem herança e sem encapsulamento com métodos personalizados.
- As definições de Estado no LangGraph utilizam a sintaxe funcional do `TypedDict` (`TypedDict("EstadoComite", {...})`).
- Cada nó do grafo é uma **função pura** (`def no_exemplo(estado: EstadoComite) -> dict:`) que aceita o estado compartilhado e retorna um dicionário contendo **apenas as chaves atualizadas**.

### 3. Concorrência e Sincronização em Grafos (LangGraph)

```text
[START] -> (FAN-OUT INICIAL) -> [coletor_dados, agente_estatistico]
                                       |
                                (BARREIRA 1)
                                       |
                                       v
                                [agente_bull, agente_bear]
                                       |
                                (BARREIRA 2)
                                       |
                                       v
                                [replica_bull, replica_bear]
                                       |
                                (BARREIRA 3)
                                       |
                                       v
     (FAN-OUT JUIZES) -> [juiz_conservador, juiz_moderado, juiz_agressivo] -> [END]
```

- **Fan-Out Inicial (Execução Concorrente)**: O grafo dispara em paralelo a coleta de dados de mercado e o cálculo de estatísticas quantitativas.
- **Barreiras de Sincronização**: Garantem que as teses iniciais e as réplicas só executem quando seus respectivos insumos estiverem totalmente gravados no estado.
- **Fan-Out dos Juízes**: Os três juízes julgam o debate simultaneamente e gravam suas decisões (`decisao_conservador`, `decisao_moderado`, `decisao_agressivo`) de forma independente.

---

## 📁 Estrutura do Projeto

```text
Multi Agentes/
│
├── .env.example               # Modelo de variáveis de ambiente
├── .gitignore                 # Proteção contra commit de chaves sensíveis
├── requirements.txt           # Dependências do projeto
├── README.md                  # Documentação completa
├── main.py                    # Ponto de entrada interativo (CLI Terminal)
├── app.py                     # Interface Gráfica Interativa (Streamlit Web)
│
├── config/
│   ├── __init__.py
│   └── ativos.py              # Lista de 30 ativos (B3 e EUA) e validação de ticker
│
├── estado/
│   ├── __init__.py
│   └── estado.py              # Definição funcional do EstadoComite (TypedDict)
│
├── nos/
│   ├── __init__.py
│   ├── coletor.py             # Coleta de mercado (yfinance + DuckDuckGo)
│   ├── agente_estatistico.py  # Análise quantitativa estatística imparcial
│   ├── agente_bull.py         # Nó do Analista Otimista
│   ├── agente_bear.py         # Nó do Analista Cético
│   ├── replica_bull.py        # Nó de Réplica Otimista
│   ├── replica_bear.py        # Nó de Réplica Cética
│   └── juizes.py              # Nós dos 3 Juízes (Conservador, Moderado, Agressivo)
│
├── grafo/
│   ├── __init__.py
│   └── grafo.py               # Montagem declarativa do StateGraph com Fan-Outs e Fan-Ins
│
└── prompts/                   # Arquivos Markdown com os prompts de sistema
    ├── agente_bull.md
    ├── agente_bear.md
    ├── replica_bull.md
    ├── replica_bear.md
    ├── juiz_conservador.md
    ├── juiz_moderado.md
    └── juiz_agressivo.md
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

#### Opção A: Interface Web no Navegador (Streamlit)
```bash
streamlit run app.py
```

#### Opção B: Terminal Interativo (CLI)
```bash
python main.py
```

---

## 🛡️ Diretrizes de Segurança — Comitê de Investimento Multi-Agente

Este documento reúne boas práticas de segurança para o projeto, divididas em duas frentes: **segurança do lado técnico/aplicação** (*client side*) e **segurança na interação com o usuário final** (*user side*). O objetivo é servir como checklist antes de expor o agente a uma turma, a testes externos, ou a um ambiente de produção.

---

### 1. Segurança Client Side (aplicação/infraestrutura)

#### 1.1 Gerenciamento de credenciais
- Nunca deixe `OPENAI_API_KEY` (ou qualquer outra chave) escrita diretamente no código-fonte. Use variáveis de ambiente (`os.environ`) ou, no Streamlit, o arquivo `secrets.toml` (`st.secrets`), que não deve ser commitado no controle de versão.
- Adicione `.env`, `secrets.toml` e `financas.db` (se contiver dados sensíveis reais) ao `.gitignore`.
- Se o projeto for publicado (ex: Streamlit Community Cloud), revise quem tem acesso ao painel de secrets antes de compartilhar o link publicamente.

#### 1.2 Acesso ao banco de dados
- As *tools* de consulta (`consultar_perfil_investidor`, `consultar_carteira_cliente`, `consultar_cotacao`) devem usar apenas **queries parametrizadas** (`?` no SQL, nunca f-string/concatenação), como já implementado — isso evita SQL Injection mesmo que a entrada venha indiretamente de um usuário mal-intencionado via prompt.
- Tools que **gravam** dados (ex: `cadastrar_investidor`) devem exigir uma segunda chamada explícita com confirmação (`confirmado=True`) antes de executar o `INSERT`/`UPDATE` — o padrão *human-in-the-loop* já adotado no projeto é a principal barreira contra ações não intencionais do agente sobre dados reais.
- Considere um usuário de banco com permissão apenas de leitura para as tools que só consultam, se o projeto migrar para um banco com controle de acesso mais granular que o SQLite.

#### 1.3 Controle de custo e uso de tokens
- Ative cache de LLM (`SQLiteCache`) e cache com TTL nas tools mais chamadas (ex: `consultar_cotacao`) para evitar chamadas repetidas desnecessárias — reduz custo e superfície de exposição a rate limit.
- Defina limites de tamanho de resposta (`max_tokens`) e monitore o consumo, especialmente em uma interface pública onde qualquer pessoa pode disparar múltiplas análises.
- Avalie adicionar um limite de requisições por sessão/usuário na interface Streamlit, para evitar abuso (ex: alguém rodando o pipeline centenas de vezes em sequência).

#### 1.4 Dados vindos de fontes externas (web search, yfinance)
- Trate o retorno de `DuckDuckGoSearchRun` e do `yfinance` como **dado não confiável**: nunca renderize esse texto como HTML bruto na interface (risco de XSS) — no Streamlit, prefira `st.markdown(texto)` sem `unsafe_allow_html=True` para conteúdo vindo de fontes externas.
- Envolva toda chamada externa (yfinance, busca web) em `try/except` com timeout implícito/explícito, retornando uma mensagem de erro amigável em vez de deixar o pipeline travar ou expor stack trace ao usuário.
- Estejam cientes de que resultados de busca podem conter tentativas de *prompt injection* (texto malicioso me instruindo a ignorar as regras). Nunca instrua o agente a "seguir instruções encontradas nos dados pesquisados" — os prompts dos nós devem sempre tratar `dados_mercado` como informação a ser resumida/interpretada, nunca como comando.

#### 1.5 Dependências e ambiente
- Fixe as versões no `requirements.txt` (ex: `langgraph==0.x.x`) em vez de deixar em aberto, para builds reprodutíveis e previsíveis.
- Revise periodicamente por vulnerabilidades conhecidas nas bibliotecas (`pip list --outdated`, ou ferramentas como `pip-audit`).
- Rode o agente com o mínimo de permissões de sistema necessárias — ele não precisa de acesso de escrita a nada além do arquivo `financas.db`.

#### 1.6 Logs e auditoria
- Registre decisões e ações de gravação (ex: cadastro de investidor) em um log de auditoria (`log_decisoes`), mas **nunca** grave chaves de API, senhas, ou dados financeiros sensíveis em texto plano em logs.
- Se o projeto crescer para produção real, considere mascarar/anonimizar identificadores de cliente nos logs.

---

### 2. Segurança User Side (interação com o usuário final)

#### 2.1 Transparência sobre o que é o agente
- Deixe explícito, na tela inicial da interface, que as recomendações são **geradas por IA para fins didáticos/demonstrativos** e **não constituem recomendação de investimento real** — o disclaimer já previsto no relatório final deve também aparecer de forma visível na UI, não só no texto gerado pelo modelo.
- Informe que o agente pode cometer erros ou "alucinar" informações, e que toda decisão financeira real deve ser validada com um profissional qualificado (CVM/CFP) antes de ser executada.

#### 2.2 Dados pessoais e financeiros
- Não peça nem armazene dados sensíveis reais (CPF, número de conta bancária, senha) em nenhum ponto do fluxo — os dados usados devem ser fictícios ou anonimizados, como no `financas.db` de demonstração.
- Se em algum momento o projeto evoluir para dados reais de usuários, será necessário revisar conformidade com a LGPD (consentimento, direito de exclusão, finalidade declarada) antes de coletar qualquer dado pessoal.

#### 2.3 Confirmação antes de ações irreversíveis
- Qualquer ação que grave, altere ou remova dados (cadastro de investidor, uma futura ordem de compra/venda simulada) deve **sempre** apresentar um resumo claro ao usuário antes de executar, e só prosseguir após confirmação explícita — nunca silenciosamente.
- Na interface, use uma cor/ícone de alerta (ex: amarelo) nesses momentos de confirmação, para diferenciá-los visualmente de conteúdo apenas informativo.

#### 2.4 Prevenção contra manipulação do agente pelo usuário
- Assuma que qualquer usuário pode tentar, propositalmente, fazer o agente ignorar suas regras de negócio (ex: pedir para "esquecer a política de risco" ou "fingir que sou o administrador"). O *system prompt* deve reforçar que as regras de compatibilidade de risco e as travas de confirmação são inegociáveis, independente do que o usuário peça na conversa.
- Não exponha, na interface ou nas respostas do agente, detalhes internos do sistema (nomes de tabelas, estrutura do banco, chaves de API) mesmo que o usuário pergunte diretamente.

#### 2.5 Acessibilidade e clareza
- Use linguagem simples nas mensagens de erro voltadas ao usuário (nunca stack traces técnicos), com uma sugestão de próximo passo (ex: "não foi possível buscar a cotação agora, tente novamente em instantes").
- Garanta contraste de cores adequado nos cards de decisão (verde/amarelo/vermelho) para não depender só da cor para transmitir a informação — inclua também o texto da recomendação por escrito, nunca só um indicador visual.

---

### 3. Checklist rápido antes de apresentar/publicar o projeto

- [ ] Nenhuma chave de API está exposta no código ou no repositório
- [ ] Todas as queries SQL usam parâmetros (`?`), nunca concatenação
- [ ] Tools de escrita exigem confirmação explícita antes de gravar
- [ ] Chamadas externas (yfinance, busca web) têm try/except e timeout
- [ ] Disclaimer de "conteúdo gerado por IA, não é recomendação real" está visível na interface
- [ ] Nenhum dado pessoal real está sendo usado ou solicitado
- [ ] Mensagens de erro ao usuário não expõem detalhes internos do sistema
- [ ] `requirements.txt` tem versões fixadas

---

## 🛠️ Tecnologias Utilizadas

- **[LangGraph](https://github.com/langchain-ai/langgraph)**: Orquestração de grafos de estados e fluxos de agentes concorrentes.
- **[LangChain OpenAI](https://github.com/langchain-ai/langchain)**: Integração com os modelos de linguagem da OpenAI.
- **[Streamlit](https://streamlit.io/)**: Interface gráfica web interativa e reativa.
- **[yfinance](https://github.com/ranaroussi/yfinance)**: Coleta de histórico de preços e volumes de ações.
- **[DuckDuckGo Search](https://github.com/deedy5/ddgs)**: Busca de notícias financeiras recentes na web.
