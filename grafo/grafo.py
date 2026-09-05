"""
================================================================================
ANÁLISE DE REFATORAÇÃO E ARQUITETURA DO GRAFO (3 JUÍZES & AGENTE ESTATÍSTICO)
================================================================================
Mudanças Arquiteturais Identificadas e Aplicadas:

1. REMOÇÃO DO JUIZ ÚNICO E CRIAÇÃO DE TRÊS NÓS DE DECISÃO PARALELOS:
   - O antigo nó 'gestor_juiz' e a chave 'decisao_final' foram removidos.
   - Foram inseridos três juízes especializados: 'juiz_conservador', 'juiz_moderado' 
     e 'juiz_agressivo', cada um gerando sua própria chave no estado 
     ('decisao_conservador', 'decisao_moderado', 'decisao_agressivo').

2. INSERÇÃO DO AGENTE ESTATÍSTICO IMPARCIAL NO FAN-OUT INICIAL:
   - O nó 'agente_estatistico' é disparado em paralelo com 'coletor_dados' a partir do START.
   - Os dados estatísticos quantitativos calculados via yfinance são integrados como insumo 
     imparcial para os analistas (Bull/Bear), réplicas e para os três Juízes.

3. FLUXO DE CONCORRÊNCIA E SINCRONIZAÇÃO EM ETAPAS:
   - Estágio 1 (Fan-Out Inicial): START -> [coletor_dados, agente_estatistico] (paralelo)
   - Estágio 2 (Barreira 1 -> Teses Iniciais): [coletor_dados, agente_estatistico] -> [agente_bull, agente_bear]
   - Estágio 3 (Barreira 2 -> Réplicas): [agente_bull, agente_bear] -> [replica_bull, replica_bear]
   - Estágio 4 (Barreira 3 -> Fan-Out de Juízes): [replica_bull, replica_bear, agente_estatistico] -> [juiz_conservador, juiz_moderado, juiz_agressivo]
   - Estágio 5 (Fim Concorrente): cada juiz finaliza conectado ao END.
================================================================================
"""

from langgraph.graph import StateGraph, START, END

from estado.estado import EstadoComite
from nos.coletor import no_coletor_dados
from nos.agente_estatistico import no_agente_estatistico
from nos.agente_bull import no_agente_bull
from nos.agente_bear import no_agente_bear
from nos.replica_bull import no_replica_bull
from nos.replica_bear import no_replica_bear
from nos.juizes import no_juiz_conservador, no_juiz_moderado, no_juiz_agressivo


def montar_grafo():
    """
    Constrói, conecta e compila o grafo estendido do Comitê de Investimento no LangGraph,
    integrando o Agente Estatístico Imparcial e os 3 Juízes por Perfil de Risco.
    """
    # 1. Instanciação do StateGraph com EstadoComite funcional
    builder = StateGraph(EstadoComite)

    # 2. Registro dos 8 nós funcionais do comitê
    builder.add_node("coletor_dados", no_coletor_dados)
    builder.add_node("agente_estatistico", no_agente_estatistico)
    builder.add_node("agente_bull", no_agente_bull)
    builder.add_node("agente_bear", no_agente_bear)
    builder.add_node("replica_bull", no_replica_bull)
    builder.add_node("replica_bear", no_replica_bear)
    builder.add_node("juiz_conservador", no_juiz_conservador)
    builder.add_node("juiz_moderado", no_juiz_moderado)
    builder.add_node("juiz_agressivo", no_juiz_agressivo)

    # 3. FAN-OUT INICIAL: Coleta de notícias e estatísticas em paralelo a partir do START
    builder.add_edge(START, "coletor_dados")
    builder.add_edge(START, "agente_estatistico")

    # 4. BARREIRA 1: Teses Iniciais (Bull e Bear) aguardam coleta de notícias e estatísticas
    builder.add_edge("coletor_dados", "agente_bull")
    builder.add_edge("agente_estatistico", "agente_bull")

    builder.add_edge("coletor_dados", "agente_bear")
    builder.add_edge("agente_estatistico", "agente_bear")

    # 5. BARREIRA 2: Réplicas aguardam ambas as teses iniciais
    builder.add_edge("agente_bull", "replica_bull")
    builder.add_edge("agente_bear", "replica_bull")

    builder.add_edge("agente_bull", "replica_bear")
    builder.add_edge("agente_bear", "replica_bear")

    # 6. BARREIRA 3: Os 3 Juízes aguardam as réplicas E os dados estatísticos
    builder.add_edge("replica_bull", "juiz_conservador")
    builder.add_edge("replica_bear", "juiz_conservador")
    builder.add_edge("agente_estatistico", "juiz_conservador")

    builder.add_edge("replica_bull", "juiz_moderado")
    builder.add_edge("replica_bear", "juiz_moderado")
    builder.add_edge("agente_estatistico", "juiz_moderado")

    builder.add_edge("replica_bull", "juiz_agressivo")
    builder.add_edge("replica_bear", "juiz_agressivo")
    builder.add_edge("agente_estatistico", "juiz_agressivo")

    # 7. Término dos 3 juízes no END
    builder.add_edge("juiz_conservador", END)
    builder.add_edge("juiz_moderado", END)
    builder.add_edge("juiz_agressivo", END)

    # 8. Compilação e retorno do grafo compilado
    return builder.compile()
