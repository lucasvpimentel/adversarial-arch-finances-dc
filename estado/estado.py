"""
Módulo de definição do Estado Compartilhado do Comitê de Investimento.
Estilo 100% funcional/procedural utilizando TypedDict funcional (sem declaração de classes).
"""

from typing import TypedDict

# Definição do estado usando a sintaxe funcional do TypedDict (sem palavra-chave class)
EstadoComite = TypedDict(
    "EstadoComite",
    {
        # Ticker do ativo financeiro a ser analisado (ex: "AAPL", "PETR4.SA", "NVDA")
        "ticker": str,
        # Dados reais de mercado e notícias coletados (preenchido pelo nó de Coleta de Dados)
        "dados_mercado": str,
        # Tese otimista inicial a favor da compra (preenchido em paralelo pelo Agente Bull)
        "argumento_bull": str,
        # Tese cética inicial de riscos e cautela (preenchido em paralelo pelo Agente Bear)
        "argumento_bear": str,
        # Réplica do Agente Bull rebatendo especificamente a tese inicial do Bear
        "replica_bull": str,
        # Réplica do Agente Bear rebatendo especificamente a tese inicial do Bull
        "replica_bear": str,
        # Veredito e síntese final do investimento (preenchido pelo Gestor/Juiz)
        "decisao_final": str,
    },
)
