"""
Módulo do Nó Coletor de Dados de Mercado.
Estilo 100% funcional/procedural utilizando funções simples (def) e manipulação de dicionários.
"""

import yfinance as yf
from langchain_community.tools import DuckDuckGoSearchRun

from estado.estado import EstadoComite


def no_coletor_dados(estado: EstadoComite) -> dict:
    """
    Nó do LangGraph responsável por coletar dados de mercado via yfinance
    e notícias recentes via DuckDuckGoSearchRun.
    
    Recebe o estado compartilhado EstadoComite e retorna APENAS o dicionário
    com a chave 'dados_mercado' para atualização parcial segura no LangGraph.
    """
    ticker_simbolo = estado.get("ticker", "").strip()
    
    try:
        # 1. Coleta de dados históricos de mercado via yfinance (período de 1 mês = "1mo")
        ticker_obj = yf.Ticker(ticker_simbolo)
        historico = ticker_obj.history(period="1mo")
        
        if historico.empty:
            resumo_financeiro = f"Não foram encontrados dados históricos para o ticker {ticker_simbolo}."
        else:
            preco_inicial = historico["Close"].iloc[0]
            preco_final = historico["Close"].iloc[-1]
            variacao_pct = ((preco_final - preco_inicial) / preco_inicial) * 100
            volume_medio = historico["Volume"].mean()
            
            resumo_financeiro = (
                f"--- DADOS FINANCEIROS (Últimos 30 dias para {ticker_simbolo}) ---\n"
                f"Preço Inicial (há 30 dias): R$/US$ {preco_inicial:.2f}\n"
                f"Preço Atual/Fechamento: R$/US$ {preco_final:.2f}\n"
                f"Variação no Período: {variacao_pct:+.2f}%\n"
                f"Volume Médio Diário: {volume_medio:,.0f} ações\n"
            )
        
        # 2. Busca de notícias recentes via DuckDuckGoSearchRun
        ferramenta_busca = DuckDuckGoSearchRun()
        query_busca = f"notícias recentes sobre a ação {ticker_simbolo} mercado financeiro"
        noticias_resultado = ferramenta_busca.run(query_busca)
        
        resumo_noticias = (
            f"--- NOTÍCIAS RECENTES DA WEB ---\n"
            f"{noticias_resultado}\n"
        )
        
        # 3. Combina dados numéricos e notícias em um texto único
        texto_final = f"{resumo_financeiro}\n{resumo_noticias}"
        
    except Exception as erro:
        # 4. Tratamento de exceções para garantir resiliência e evitar queda da aplicação
        texto_final = (
            f"Dados de mercado e notícias indisponíveis no momento para {ticker_simbolo} "
            f"devido a instabilidade na conexão ou nas APIs. (Erro: {str(erro)})"
        )
    
    # 5. Retorna APENAS a chave atualizada para fusão limpa no LangGraph
    return {"dados_mercado": texto_final}
