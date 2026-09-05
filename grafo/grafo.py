"""
================================================================================
ANÁLISE DE REFATORAÇÃO E ARQUITETURA DO GRAFO (ETAPA DE RÉPLICAS)
================================================================================
Mudanças Arquiteturais Identificadas e Aplicadas:

1. REESTRUTURAÇÃO DO FAN-IN / FAN-OUT ORIGINAL:
   - Na versão anterior, 'agente_bull' e 'agente_bear' convergiam diretamente em um Fan-In
     único para o 'gestor_juiz'.
   - Com a introdução da rodada de réplicas, NÃO é possível prolongar o Fan-Out original
     sem uma barreira de sincronização intermediária. O motivo é que 'replica_bull' precisa 
     do 'argumento_bear' (e 'replica_bear' precisa do 'argumento_bull'). Se 'replica_bull' 
     rodasse antes do 'agente_bear' concluir, a chave 'argumento_bear' estaria ausente ou vazia.
   - Solução de Refatoração: Criou-se um PONTO DE SINCRONIZAÇÃO INTERMEDIÁRIO. As saídas de 
     'agente_bull' E 'agente_bear' agora convergem para 'replica_bull' E 'replica_bear', 
     garantindo que a segunda rodada (Fan-Out 2) só inicie com o estado 100% preenchido.

2. INCLUSÃO DE NOVOS NÓS E CONEXÃO EM DUAS ETAPAS (FAN-IN 1 -> FAN-OUT 2 -> FAN-IN 2):
   - Estágio 1 (Coleta): START -> coletor_dados
   - Estágio 2 (Fan-Out 1): coletor_dados -> [agente_bull, agente_bear] (em paralelo)
   - Estágio 3 (Sincronização Intermediária -> Fan-Out 2): [agente_bull, agente_bear] -> [replica_bull, replica_bear]
   - Estágio 4 (Fan-In 2): [replica_bull, replica_bear] -> gestor_juiz
   - Estágio 5 (Fim): gestor_juiz -> END

3. DESACOPLAMENTO E MANUTENÇÃO DA ISOLAMENTO DOS NÓS:
   - Todos os nós continuam sendo funções puras retornando dicionários parciais 
     ({"replica_bull": ...}, {"replica_bear": ...}), permitindo que o LangGraph faça
     o merge automático e concorrente do estado compartilhado EstadoComite.
================================================================================
"""

from langgraph.graph import StateGraph, START, END

from estado.estado import EstadoComite
from nos.coletor import no_coletor_dados
from nos.agente_bull import no_agente_bull
from nos.agente_bear import no_agente_bear
from nos.replica_bull import no_replica_bull
from nos.replica_bear import no_replica_bear
from nos.gestor_juiz import no_gestor_juiz


def montar_grafo():
    """
    Constrói, conecta e compila o grafo estendido do Comitê de Investimento no LangGraph,
    incluindo a rodada de réplicas com barreira de sincronização intermediária.
    
    FLUXO COMPLETO DO GRAFO DE AGENTES:
    
    [START] -> coletor_dados -> (FAN-OUT 1) -> [agente_bull] --\
                                            -> [agente_bear] ---+-> (SINCRONIZAÇÃO INTERMEDIÁRIA)
                                                                      |
                                            /-------------------------/
                                            |
                                            +-> (FAN-OUT 2) -> [replica_bull] --\
                                                            -> [replica_bear] ---+-> (FAN-IN 2) -> gestor_juiz -> [END]
    """
    # 1. Instanciação do StateGraph com EstadoComite funcional
    builder = StateGraph(EstadoComite)

    # 2. Registro dos 6 nós do comitê de investimento
    builder.add_node("coletor_dados", no_coletor_dados)
    builder.add_node("agente_bull", no_agente_bull)
    builder.add_node("agente_bear", no_agente_bear)
    builder.add_node("replica_bull", no_replica_bull)
    builder.add_node("replica_bear", no_replica_bear)
    builder.add_node("gestor_juiz", no_gestor_juiz)

    # 3. Ponto de entrada inicial
    builder.add_edge(START, "coletor_dados")

    # 4. FAN-OUT 1: Coleta -> Teses Iniciais (Bull e Bear em paralelo)
    builder.add_edge("coletor_dados", "agente_bull")
    builder.add_edge("coletor_dados", "agente_bear")

    # 5. SINCRONIZAÇÃO INTERMEDIÁRIA & FAN-OUT 2:
    # Ambas as teses iniciais devem concluir antes de acionar as réplicas
    builder.add_edge("agente_bull", "replica_bull")
    builder.add_edge("agente_bear", "replica_bull")

    builder.add_edge("agente_bull", "replica_bear")
    builder.add_edge("agente_bear", "replica_bear")

    # 6. FAN-IN 2: Ambas as réplicas convergem para o Gestor / Juiz
    builder.add_edge("replica_bull", "gestor_juiz")
    builder.add_edge("replica_bear", "gestor_juiz")

    # 7. Término do grafo
    builder.add_edge("gestor_juiz", END)

    # 8. Compilação e retorno do grafo compilado
    return builder.compile()
