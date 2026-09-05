"""
Módulo de Cadastro e Validação de Ativos Pré-definidos.
Estilo 100% funcional/procedural utilizando constantes (listas de dicionários) e funções simples (def).
"""

# Lista de 15 ações brasileiras da B3
ATIVOS_NACIONAIS = [
    {"ticker": "PETR4.SA", "nome": "Petrobras PN", "setor": "Petróleo e Gás"},
    {"ticker": "VALE3.SA", "nome": "Vale S.A.", "setor": "Mineração"},
    {"ticker": "ITUB4.SA", "nome": "Itaú Unibanco PN", "setor": "Bancos"},
    {"ticker": "BBDC4.SA", "nome": "Bradesco PN", "setor": "Bancos"},
    {"ticker": "ABEV3.SA", "nome": "Ambev S.A.", "setor": "Bebidas/Consumo"},
    {"ticker": "WEGE3.SA", "nome": "WEG S.A.", "setor": "Bens de Capital"},
    {"ticker": "MGLU3.SA", "nome": "Magazine Luiza S.A.", "setor": "Varejo"},
    {"ticker": "B3SA3.SA", "nome": "B3 S.A.", "setor": "Bolsa de Valores"},
    {"ticker": "RENT3.SA", "nome": "Localiza Rent a Car", "setor": "Aluguel de Veículos"},
    {"ticker": "SUZB3.SA", "nome": "Suzano S.A.", "setor": "Papel e Celulose"},
    {"ticker": "EGIE3.SA", "nome": "Engie Brasil", "setor": "Energia Elétrica"},
    {"ticker": "JBSS3.SA", "nome": "JBS S.A.", "setor": "Alimentos"},
    {"ticker": "GGBR4.SA", "nome": "Gerdau PN", "setor": "Siderurgia"},
    {"ticker": "LREN3.SA", "nome": "Lojas Renner", "setor": "Varejo/Moda"},
    {"ticker": "RADL3.SA", "nome": "Raia Drogasil", "setor": "Farmácias"},
]

# Lista de 15 ações norte-americanas (EUA)
ATIVOS_INTERNACIONAIS = [
    {"ticker": "AAPL", "nome": "Apple Inc.", "setor": "Tecnologia"},
    {"ticker": "MSFT", "nome": "Microsoft Corp.", "setor": "Tecnologia"},
    {"ticker": "GOOGL", "nome": "Alphabet Inc.", "setor": "Tecnologia"},
    {"ticker": "AMZN", "nome": "Amazon.com Inc.", "setor": "E-commerce"},
    {"ticker": "TSLA", "nome": "Tesla Inc.", "setor": "Automotivo/Energia"},
    {"ticker": "NVDA", "nome": "Nvidia Corp.", "setor": "Semicondutores"},
    {"ticker": "META", "nome": "Meta Platforms Inc.", "setor": "Tecnologia/Redes Sociais"},
    {"ticker": "JPM", "nome": "JPMorgan Chase", "setor": "Bancos"},
    {"ticker": "KO", "nome": "Coca-Cola Co.", "setor": "Bebidas/Consumo"},
    {"ticker": "JNJ", "nome": "Johnson & Johnson", "setor": "Saúde/Farmacêutica"},
    {"ticker": "DIS", "nome": "Walt Disney Co.", "setor": "Entretenimento"},
    {"ticker": "NKE", "nome": "Nike Inc.", "setor": "Vestuário/Esporte"},
    {"ticker": "V", "nome": "Visa Inc.", "setor": "Serviços Financeiros"},
    {"ticker": "PG", "nome": "Procter & Gamble", "setor": "Bens de Consumo"},
    {"ticker": "XOM", "nome": "Exxon Mobil Corp.", "setor": "Petróleo e Gás"},
]

# Lista unificada contendo todos os 30 ativos pré-definidos
ATIVOS_PREDEFINIDOS = ATIVOS_NACIONAIS + ATIVOS_INTERNACIONAIS


def validar_ticker(ticker: str) -> bool:
    """
    Verifica se o ticker fornecido está presente na lista de ATIVOS_PREDEFINIDOS.
    
    A busca é insensível a maiúsculas/minúsculas e remove espaços extras.
    Retorna True se for válido, ou False caso contrário.
    """
    ticker_limpo = ticker.strip().upper()
    for ativo in ATIVOS_PREDEFINIDOS:
        if ativo["ticker"].upper() == ticker_limpo:
            return True
    return False
