"""
Ponto de Entrada Principal (CLI) do Comitê de Investimento Multi-Agente.
Estilo 100% funcional/procedural com funções simples (def) e controle de fluxo interativo.
"""

import sys

# Garante suporte a caracteres UTF-8 (emojis) no terminal Windows (cmd / powershell)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from config.ativos import ATIVOS_NACIONAIS, ATIVOS_INTERNACIONAIS, validar_ticker
from grafo.grafo import montar_grafo


def exibir_menu_ativos():
    """
    Exibe de forma organizada os ativos disponíveis para análise,
    separando visualmente por mercado (Nacionais vs Internacionais).
    """
    print("\n" + "=" * 80)
    print("           COMITÊ DE INVESTIMENTO MULTI-AGENTE - ATIVOS DISPONÍVEIS           ")
    print("=" * 80)

    print("\n🇧🇷 ATIVOS NACIONAIS (B3 - Brasil):")
    print("-" * 80)
    for ativo in ATIVOS_NACIONAIS:
        print(f"  • {ativo['ticker']:<10} | {ativo['nome']:<25} | Setor: {ativo['setor']}")

    print("\n🇺🇸 ATIVOS INTERNACIONAIS (EUA):")
    print("-" * 80)
    for ativo in ATIVOS_INTERNACIONAIS:
        print(f"  • {ativo['ticker']:<10} | {ativo['nome']:<25} | Setor: {ativo['setor']}")

    print("=" * 80)


def exibir_resultado_comite(resultado: dict):
    """
    Exibe o debate completo, a análise estatística quantitativa e os relatórios dos 3 Juízes
    (Conservador, Moderado e Agressivo) formatados em blocos estruturados.
    """
    ticker = resultado.get("ticker", "DESCONHECIDO")
    
    print("\n" + "#" * 80)
    print(f"       RELATÓRIO COMPLETO DO COMITÊ DE INVESTIMENTO PARA: {ticker}")
    print("#" * 80)

    print("\n📊 1. DADOS DE MERCADO COLETADOS (yfinance + Notícias Web)")
    print("-" * 80)
    print(resultado.get("dados_mercado", "Sem dados de mercado."))

    print("\n📈 2. ANÁLISE ESTATÍSTICA QUANTITATIVA IMPARCIAL")
    print("-" * 80)
    print(resultado.get("dados_estatisticos", "Sem dados estatísticos."))

    print("\n🐂 3. TESE INICIAL DO ANALISTA BULL (OTIMISTA)")
    print("-" * 80)
    print(resultado.get("argumento_bull", "Sem argumento Bull."))

    print("\n🐻 4. TESE INICIAL DO ANALISTA BEAR (CÉTICO/RISCO)")
    print("-" * 80)
    print(resultado.get("argumento_bear", "Sem argumento Bear."))

    print("\n🔄 5. RÉPLICA DO ANALISTA BULL (REBATENDO O BEAR)")
    print("-" * 80)
    print(resultado.get("replica_bull", "Sem réplica Bull."))

    print("\n🔄 6. RÉPLICA DO ANALISTA BEAR (REBATENDO O BULL)")
    print("-" * 80)
    print(resultado.get("replica_bear", "Sem réplica Bear."))

    print("\n" + "=" * 80)
    print("                     PARECERES DOS 3 JUÍZES POR PERFIL DE RISCO                     ")
    print("=" * 80)

    print("\n🛡️ 7. PARECER DO JUIZ CONSERVADOR (Preservação de Capital & Baixa Volatilidade)")
    print("-" * 80)
    print(resultado.get("decisao_conservador", "Sem parecer conservador."))

    print("\n⚖️ 8. PARECER DO JUIZ MODERADO (Equilíbrio Risco vs Retorno)")
    print("-" * 80)
    print(resultado.get("decisao_moderado", "Sem parecer moderado."))

    print("\n🚀 9. PARECER DO JUIZ AGRESSIVO (Maximização de Retorno & Tolerância a Risco)")
    print("-" * 80)
    print(resultado.get("decisao_agressivo", "Sem parecer agressivo."))

    print("=" * 80 + "\n")


def executar_pipeline():
    """
    Função principal que gerencia a compilação do grafo, o loop de interação
    com o usuário, a validação das entradas e a invocação do LangGraph.
    """
    print("\nInicializando o Grafo do Comitê de Investimento no LangGraph...")
    pipeline = montar_grafo()
    print("Grafo compilado com sucesso!\n")

    while True:
        exibir_menu_ativos()

        ticker_input = input("\nDigite o Ticker do ativo que deseja analisar (ou 'sair' para encerrar): ").strip()

        if ticker_input.lower() in ["sair", "exit", "0", "q"]:
            print("\nEncerrando o Comitê de Investimento. Até logo!")
            break

        if not validar_ticker(ticker_input):
            print(f"\n❌ Ticker '{ticker_input}' inválido ou não presente na lista pré-definida.")
            print("Por favor, selecione um ticker válido mostrado no menu ou digite 'sair'.")
            input("\nPressione ENTER para tentar novamente...")
            continue

        ticker_validado = ticker_input.upper()
        print(f"\n🚀 Iniciando análise do Comitê de Investimento para {ticker_validado}...")
        print("Aguarde: Coletando dados, calculando estatísticas, rodando análises em paralelo e processando o debate...\n")

        # Invocação do pipeline compilado do LangGraph
        resultado_final = pipeline.invoke({"ticker": ticker_validado})

        # Exibição completa do debate, estatísticas e 3 decisões
        exibir_resultado_comite(resultado_final)

        opcao = input("Deseja analisar outro ativo? (s/n): ").strip().lower()
        if opcao not in ["s", "sim", "y", "yes"]:
            print("\nEncerrando o Comitê de Investimento. Até logo!")
            break


if __name__ == "__main__":
    executar_pipeline()
