"""
Módulo do Nó Agente Estatístico Imparcial.
Estilo 100% funcional/procedural utilizando funções simples (def) e manipulação de dicionários.
"""

import yfinance as yf
from estado.estado import EstadoComite


def no_agente_estatistico(estado: EstadoComite) -> dict:
    """
    Nó do LangGraph responsável por calcular métricas quantitativas imparciais do ativo.
    
    POR QUE O AGENTE ESTATÍSTICO DEVE PERMANECER IMPARCIAL (SEM OPINIÃO):
    O papel deste agente é fornecer fatos matemáticos puros e estatísticas objetivas,
    sem nenhum viés, recomendação ou interpretação qualitativa. Ele serve como insumo
    inquestionável tanto para os analistas de debate (Bull e Bear) formularem seus 
    argumentos numéricos, quanto para os três Juízes ponderarem os riscos matemáticos.
    
    Retorna APENAS o dicionário com a chave 'dados_estatisticos'.
    """
    ticker_simbolo = estado.get("ticker", "").strip()

    try:
        # Busca 3 meses de histórico ("3mo") para calcular janelas de 7, 30 e 90 dias
        ticker_obj = yf.Ticker(ticker_simbolo)
        historico = ticker_obj.history(period="3mo")

        if historico.empty:
            texto_estatistico = f"Dados estatísticos indisponíveis para o ticker {ticker_simbolo}."
        else:
            preco_atual = historico["Close"].iloc[-1]
            volume_medio_30d = historico["Volume"].tail(22).mean()

            # 1. Variações percentuais em diferentes janelas (7d, 30d, 90d)
            var_7d = ((preco_atual - historico["Close"].iloc[-6]) / historico["Close"].iloc[-6]) * 100 if len(historico) >= 6 else 0.0
            var_30d = ((preco_atual - historico["Close"].iloc[-22]) / historico["Close"].iloc[-22]) * 100 if len(historico) >= 22 else 0.0
            var_90d = ((preco_atual - historico["Close"].iloc[0]) / historico["Close"].iloc[0]) * 100 if len(historico) > 0 else 0.0

            # 2. Volatilidade (desvio padrão dos retornos percentuais diários nos últimos 30 dias)
            retornos_diarios = historico["Close"].tail(22).pct_change().dropna()
            volatilidade_30d = retornos_diarios.std() * 100

            # 3. Médias Móveis Simples (SMA-7 e SMA-30)
            sma_7 = historico["Close"].tail(7).mean()
            sma_30 = historico["Close"].tail(22).mean()

            texto_estatistico = (
                f"--- ANÁLISE ESTATÍSTICA QUANTITATIVA IMPARCIAL ({ticker_simbolo}) ---\n"
                f"• Preço de Fechamento Atual: R$/US$ {preco_atual:.2f}\n"
                f"• Variação Percentual (7 dias): {var_7d:+.2f}%\n"
                f"• Variação Percentual (30 dias): {var_30d:+.2f}%\n"
                f"• Variação Percentual (90 dias): {var_90d:+.2f}%\n"
                f"• Volatilidade Diária (30d - Desvio Padrão): {volatilidade_30d:.2f}%\n"
                f"• Volume Médio Diário (30d): {volume_medio_30d:,.0f} ações\n"
                f"• Média Móvel Simples (SMA 7d): R$/US$ {sma_7:.2f}\n"
                f"• Média Móvel Simples (SMA 30d): R$/US$ {sma_30:.2f}\n"
                f"• Distância do Preço vs SMA 30d: {((preco_atual - sma_30) / sma_30) * 100:+.2f}%\n"
            )

    except Exception as erro:
        texto_estatistico = (
            f"Falha ao calcular estatísticas quantitativas para {ticker_simbolo} "
            f"via yfinance. (Erro: {str(erro)})"
        )

    # Retorna APENAS a chave atualizada no estado global do LangGraph
    return {"dados_estatisticos": texto_estatistico}
