"""
===============================================================================
COMITÊ DE INVESTIMENTO MULTI-AGENTE - INTERFACE GRÁFICA INTERATIVA (STREAMLIT)
===============================================================================
Desenvolvido em estilo 100% funcional/procedural com funções simples (def).
Reaproveita a orquestração em grafo do LangGraph e exibe o debate adversarial
em tempo real com os 3 Juízes por Perfil de Risco e o Agente Estatístico.
"""

import time
import streamlit as st
from config.ativos import ATIVOS_NACIONAIS, ATIVOS_INTERNACIONAIS, ATIVOS_PREDEFINIDOS, validar_ticker
from grafo.grafo import montar_grafo


@st.cache_resource
def obter_pipeline():
    """
    Carrega e compila o grafo do LangGraph uma única vez,
    armazenando em cache via @st.cache_resource para reaproveitamento.
    """
    return montar_grafo()


def injetar_css_customizado():
    """
    Injeta CSS customizado para criar uma interface bonita, moderna e profissional,
    com paleta de cores harmoniosa, cards com sombras suaves e badges de decisão.
    """
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', sans-serif;
        }

        /* Estilização do cabeçalho principal */
        .main-header {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            padding: 24px;
            border-radius: 16px;
            color: #ffffff;
            margin-bottom: 24px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .main-header h1 {
            color: #38bdf8;
            font-weight: 800;
            font-size: 2.2rem;
            margin-bottom: 8px;
        }

        .main-header p {
            color: #94a3b8;
            font-size: 1.05rem;
            margin: 0;
        }

        /* Cards visuais dos agentes */
        .card-agent {
            background-color: #1e293b;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 16px;
            border: 1px solid #334155;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }

        .card-bull {
            border-left: 6px solid #22c55e;
            background: linear-gradient(135deg, rgba(34, 197, 94, 0.05) 0%, rgba(30, 41, 59, 1) 100%);
        }

        .card-bear {
            border-left: 6px solid #ef4444;
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.05) 0%, rgba(30, 41, 59, 1) 100%);
        }

        .card-stat {
            border-left: 6px solid #38bdf8;
            background: linear-gradient(135deg, rgba(56, 189, 248, 0.05) 0%, rgba(30, 41, 59, 1) 100%);
        }

        /* Cards de Decisão dos Juízes */
        .card-juiz {
            border-radius: 14px;
            padding: 20px;
            min-height: 380px;
            border: 1px solid #334155;
            box-shadow: 0 8px 16px -4px rgba(0, 0, 0, 0.2);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }

        .card-conservador {
            border-top: 5px solid #60a5fa;
            background: linear-gradient(180deg, rgba(96, 165, 250, 0.08) 0%, rgba(15, 23, 42, 0.95) 100%);
        }

        .card-moderado {
            border-top: 5px solid #f59e0b;
            background: linear-gradient(180deg, rgba(245, 158, 11, 0.08) 0%, rgba(15, 23, 42, 0.95) 100%);
        }

        .card-agressivo {
            border-top: 5px solid #a855f7;
            background: linear-gradient(180deg, rgba(168, 85, 247, 0.08) 0%, rgba(15, 23, 42, 0.95) 100%);
        }

        /* Badges de decisão (Comprar, Aguardar, Evitar) */
        .badge-decisao {
            display: inline-block;
            padding: 6px 16px;
            border-radius: 20px;
            font-weight: 800;
            font-size: 0.95rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 12px;
        }

        .badge-comprar {
            background-color: rgba(34, 197, 94, 0.2);
            color: #4ade80;
            border: 1px solid #22c55e;
        }

        .badge-aguardar {
            background-color: rgba(245, 158, 11, 0.2);
            color: #fbbf24;
            border: 1px solid #f59e0b;
        }

        .badge-evitar {
            background-color: rgba(239, 68, 68, 0.2);
            color: #f87171;
            border: 1px solid #ef4444;
        }

        .badge-confianca {
            font-size: 0.8rem;
            color: #94a3b8;
            font-weight: 600;
            margin-left: 8px;
        }

        /* Diagrama de fluxo visual da tela inicial */
        .flow-container {
            display: flex;
            justify-content: space-around;
            align-items: center;
            background-color: #0f172a;
            padding: 20px;
            border-radius: 14px;
            border: 1px solid #334155;
            margin: 20px 0;
        }

        .flow-step {
            text-align: center;
            padding: 12px;
            background-color: #1e293b;
            border-radius: 10px;
            border: 1px solid #475569;
            width: 18%;
        }

        .flow-arrow {
            font-size: 1.5rem;
            color: #38bdf8;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )


def extrair_decisao_e_confianca(texto_juiz: str) -> tuple[str, str]:
    """
    Analisa o texto retornado pelo LLM do juiz para extrair a decisão
    (COMPRAR, AGUARDAR ou EVITAR) e o nível de confiança (Baixo, Médio, Alto).
    """
    texto_upper = texto_juiz.upper()
    
    decisao = "AGUARDAR"
    if "COMPRAR" in texto_upper:
        decisao = "COMPRAR"
    elif "EVITAR" in texto_upper:
        decisao = "EVITAR"
    elif "AGUARDAR" in texto_upper:
        decisao = "AGUARDAR"

    confianca = "MÉDIO"
    if "CONFIAÇÃO: ALTO" in texto_upper or "CONFIANÇA: ALTO" in texto_upper or "ALTO" in texto_upper:
        confianca = "ALTO"
    elif "CONFIAÇÃO: BAIXO" in texto_upper or "CONFIANÇA: BAIXO" in texto_upper or "BAIXO" in texto_upper:
        confianca = "BAIXO"

    return decisao, confianca


def renderizar_card_juiz(titulo: str, icone: str, perfil_desc: str, texto_juiz: str, classe_css: str):
    """
    Renderiza um card visualmente destacado para o parecer de um dos três juízes,
    com badge colorido conforme a decisão (Verde=Comprar, Amarelo=Aguardar, Vermelho=Evitar).
    """
    decisao, confianca = extrair_decisao_e_confianca(texto_juiz)
    
    badge_classe = "badge-aguardar"
    if decisao == "COMPRAR":
        badge_classe = "badge-comprar"
    elif decisao == "EVITAR":
        badge_classe = "badge-evitar"

    st.markdown(
        f"""
        <div class="card-juiz {classe_css}">
            <div>
                <h3>{icone} {titulo}</h3>
                <p style="color: #94a3b8; font-size: 0.85rem; margin-bottom: 12px;">{perfil_desc}</p>
                <div>
                    <span class="badge-decisao {badge_classe}">{decisao}</span>
                    <span class="badge-confianca">Confiança: <b>{confianca}</b></span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.expander(f"📖 Ver Justificativa Completa do {titulo}", expanded=True):
        st.markdown(texto_juiz)


def renderizar_boas_vindas():
    """
    Exibe a tela inicial de boas-vindas com o diagrama do fluxo multi-agente
    e orientações sobre como utilizar a plataforma.
    """
    st.markdown(
        """
        <div class="main-header">
            <h1>🏛️ Comitê de Investimento Multi-Agente</h1>
            <p>Plataforma didática de análise financeira com debate adversarial orquestrado via <b>LangGraph</b>.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### 🧩 Como Funciona o Comitê de IA?")
    st.markdown(
        """
        Em vez de confiar em um único modelo de linguagem que pode sofrer de viés de confirmação, 
        nosso comitê utiliza **8 agentes de IA operando em rede** para analisar o ativo sob múltiplos pontos de vista:
        """
    )

    st.markdown(
        """
        <div class="flow-container">
            <div class="flow-step">
                <div style="font-size: 1.8rem;">🌐 📊</div>
                <b>Coleta & Estatísticas</b>
                <div style="font-size: 0.75rem; color: #94a3b8;">yfinance + Notícias + Métricas 30d/90d</div>
            </div>
            <div class="flow-arrow">➔</div>
            <div class="flow-step">
                <div style="font-size: 1.8rem;">🐂 🆚 🐻</div>
                <b>Teses Iniciais</b>
                <div style="font-size: 0.75rem; color: #94a3b8;">Agente Bull vs Agente Bear em paralelo</div>
            </div>
            <div class="flow-arrow">➔</div>
            <div class="flow-step">
                <div style="font-size: 1.8rem;">🔄 🔄</div>
                <b>Réplicas</b>
                <div style="font-size: 0.75rem; color: #94a3b8;">Rebatimento mútuo de argumentos</div>
            </div>
            <div class="flow-arrow">➔</div>
            <div class="flow-step">
                <div style="font-size: 1.8rem;">🛡️ ⚖️ 🚀</div>
                <b>3 Juízes</b>
                <div style="font-size: 0.75rem; color: #94a3b8;">Conservador, Moderado e Agressivo</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.info("👈 **Para começar:** Selecione um ativo na barra lateral e clique no botão **Analisar Ativo**!")


def renderizar_debate(resultado: dict):
    """
    Exibe os dados de mercado, estatísticas e o debate adversarial em abas organizadas.
    """
    st.markdown(f"## 📋 Relatório de Análise: **{resultado.get('ticker')}**")

    tab_dados, tab_debate, tab_juizes = st.tabs([
        "📊 Dados de Mercado & Estatísticas",
        "⚔️ Debate Adversarial (Bull vs Bear)",
        "👨‍⚖️ Pareceres dos 3 Juízes"
    ])

    with tab_dados:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 🌐 Dados de Mercado & Notícias Coletadas")
            st.info(resultado.get("dados_mercado", "Sem dados de mercado."))
        with col2:
            st.markdown("### 📈 Análise Estatística Quantitativa (Imparcial)")
            st.success(resultado.get("dados_estatisticos", "Sem dados estatísticos."))

    with tab_debate:
        st.markdown("### 1️⃣ Primeira Rodada: Teses Iniciais")
        col_bull1, col_bear1 = st.columns(2)
        with col_bull1:
            st.markdown(
                """
                <div class="card-agent card-bull">
                    <h4>🐂 Tese Inicial do Agente Bull (Otimista)</h4>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.write(resultado.get("argumento_bull"))

        with col_bear1:
            st.markdown(
                """
                <div class="card-agent card-bear">
                    <h4>🐻 Tese Inicial do Agente Bear (Cético / Risco)</h4>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.write(resultado.get("argumento_bear"))

        st.divider()

        st.markdown("### 2️⃣ Segunda Rodada: Réplicas e Rebatimentos")
        col_bull2, col_bear2 = st.columns(2)
        with col_bull2:
            st.markdown(
                """
                <div class="card-agent card-bull">
                    <h4>🔄 Réplica do Agente Bull (Rebatendo o Bear)</h4>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.write(resultado.get("replica_bull"))

        with col_bear2:
            st.markdown(
                """
                <div class="card-agent card-bear">
                    <h4>🔄 Réplica do Agente Bear (Rebatendo o Bull)</h4>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.write(resultado.get("replica_bear"))

    with tab_juizes:
        st.markdown("### ⚖️ Julgamento Imparcial por Perfil de Risco")
        st.caption("Veja como o mesmo debate leva a pareceres distintos conforme o apetite de risco do investidor:")
        
        col_cons, col_mod, col_agr = st.columns(3)

        with col_cons:
            renderizar_card_juiz(
                titulo="Juiz Conservador",
                icone="🛡️",
                perfil_desc="Prioriza Preservação de Capital e Baixa Volatilidade",
                texto_juiz=resultado.get("decisao_conservador", ""),
                classe_css="card-conservador"
            )

        with col_mod:
            renderizar_card_juiz(
                titulo="Juiz Moderado",
                icone="⚖️",
                perfil_desc="Busca Equilíbrio Risco vs Retorno",
                texto_juiz=resultado.get("decisao_moderado", ""),
                classe_css="card-moderado"
            )

        with col_agr:
            renderizar_card_juiz(
                titulo="Juiz Agressivo",
                icone="🚀",
                perfil_desc="Prioriza Potencial de Retorno e Tolerância a Risco",
                texto_juiz=resultado.get("decisao_agressivo", ""),
                classe_css="card-agressivo"
            )


def executar_simulacao(ticker_selecionado: str):
    """
    Executa a invocação do pipeline compilado do LangGraph com um feedback
    visual elaborado que indica o progresso em tempo real de cada estágio do grafo.
    """
    pipeline = obter_pipeline()

    with st.status(f"🚀 Executando Comitê de Investimento para **{ticker_selecionado}**...", expanded=True) as status:
        st.write("🌐 **Estágio 1/4:** Coletando notícias web e histórico do yfinance...")
        time.sleep(0.5)

        st.write("📈 **Estágio 2/4:** Calculando indicadores quantitativos (volatilidade, retornos, médias móveis)...")
        time.sleep(0.5)

        st.write("🐂 🐻 **Estágio 3/4:** Rodando agentes Bull e Bear em paralelo (Teses + Réplicas)...")
        
        # Invocação real do pipeline do LangGraph
        inicio = time.time()
        try:
            resultado = pipeline.invoke({"ticker": ticker_selecionado})
            duracao = time.time() - inicio

            st.write("🛡️ ⚖️ 🚀 **Estágio 4/4:** Processando pareceres da banca dos 3 Juízes...")
            status.update(label=f"✅ Análise concluída com sucesso em {duracao:.1f} segundos!", state="complete", expanded=False)

            # Salva no histórico de sessão (session_state)
            if "historico" not in st.session_state:
                st.session_state["historico"] = {}
            st.session_state["historico"][ticker_selecionado] = resultado
            st.session_state["analise_atual"] = resultado

        except Exception as erro:
            status.update(label="❌ Falha durante o processamento do pipeline.", state="error")
            st.error(f"Ocorreu um erro ao processar a análise para {ticker_selecionado}: {str(erro)}")


def main():
    """
    Função principal de orquestração da interface do Streamlit.
    """
    st.set_page_config(
        page_title="Comitê de Investimento Multi-Agente",
        page_icon="🏛️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    injetar_css_customizado()

    # Inicializa o histórico na sessão se não existir
    if "historico" not in st.session_state:
        st.session_state["historico"] = {}

    # Sidebar - Seleção de Ativos e Histórico
    st.sidebar.title("📌 Painel de Controle")
    st.sidebar.markdown("---")

    tipo_mercado = st.sidebar.radio(
        "Selecione o Mercado:",
        ["🇧🇷 Ações Nacionais (B3)", "🇺🇸 Ações Internacionais (EUA)"]
    )

    if "Nacionais" in tipo_mercado:
        lista_ativos = ATIVOS_NACIONAIS
    else:
        lista_ativos = ATIVOS_INTERNACIONAIS

    opcoes_formatadas = {
        f"{a['ticker']} - {a['nome']} ({a['setor']})": a['ticker']
        for a in lista_ativos
    }

    ativo_escolhido_label = st.sidebar.selectbox(
        "Escolha o Ativo:",
        options=list(opcoes_formatadas.keys())
    )

    ticker_selecionado = opcoes_formatadas[ativo_escolhido_label]

    st.sidebar.markdown("---")

    if st.sidebar.button("🚀 Analisar Ativo", use_container_width=True, type="primary"):
        executar_simulacao(ticker_selecionado)

    # Histórico de Análises Anteriores na Sidebar
    if st.session_state["historico"]:
        st.sidebar.markdown("---")
        st.sidebar.subheader("📜 Histórico da Sessão")
        st.sidebar.caption("Clique para rever uma análise anterior sem gastar créditos de API:")
        
        for tkr in list(st.session_state["historico"].keys()):
            if st.sidebar.button(f"📊 Ver análise de {tkr}", key=f"hist_{tkr}", use_container_width=True):
                st.session_state["analise_atual"] = st.session_state["historico"][tkr]

    # Exibição Principal no Corpo da Página
    if "analise_atual" in st.session_state:
        renderizar_debate(st.session_state["analise_atual"])
    else:
        renderizar_boas_vindas()


if __name__ == "__main__":
    main()
