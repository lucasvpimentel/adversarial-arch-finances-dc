"""
Módulo do Nó Réplica Bear (Réplica Cética/Conservadora).
Estilo 100% funcional/procedural utilizando funções simples (def) e manipulação de dicionários.
"""

import os
import httpx
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI

from estado.estado import EstadoComite

# Carrega as variáveis de ambiente estritamente do arquivo .env
load_dotenv()


def carregar_prompt(caminho_arquivo: str) -> str:
    """
    Função utilitária simples para ler o conteúdo de um arquivo de prompt markdown.
    """
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        return f.read()


def no_replica_bear(estado: EstadoComite) -> dict:
    """
    Nó do LangGraph responsável pela RÉPLICA CÉTICA / CONSERVADORA (Bear).
    
    Consome 'dados_mercado', 'dados_estatisticos' e 'argumento_bull'.
    Retorna APENAS o dicionário com a chave 'replica_bear'.
    """
    ticker = estado.get("ticker", "Ativo")
    dados_mercado = estado.get("dados_mercado", "Sem dados disponíveis.")
    dados_estatisticos = estado.get("dados_estatisticos", "Sem dados estatísticos.")
    argumento_bull = estado.get("argumento_bull", "Sem argumento Bull inicial.")

    # Leitura direta das configurações do .env
    modelo_nome = os.getenv("OPENAI_MODEL")
    temperatura = float(os.getenv("TEMPERATURE", "0.2"))
    api_key = os.getenv("OPENAI_API_KEY")

    # Inicialização do LLM usando estritamente as configurações do .env e httpx.Client() para resiliência de rede
    llm = ChatOpenAI(
        model=modelo_nome,
        temperature=temperatura,
        api_key=api_key,
        http_client=httpx.Client()
    )

    # Carrega o prompt de sistema a partir do arquivo .md na pasta prompts/
    caminho_prompt = os.path.join("prompts", "replica_bear.md")
    conteudo_prompt_sistema = carregar_prompt(caminho_prompt)

    mensagem_sistema = SystemMessage(content=conteudo_prompt_sistema)

    mensagem_usuario = HumanMessage(
        content=(
            f"ATIVO ANALISADO: {ticker}\n\n"
            f"1. DADOS DE MERCADO E NOTÍCIAS:\n"
            f"'''\n{dados_mercado}\n'''\n\n"
            f"2. ANÁLISE ESTATÍSTICA QUANTITATIVA IMPARCIAL:\n"
            f"'''\n{dados_estatisticos}\n'''\n\n"
            f"3. TESE INICIAL DO ANALISTA BULL (OTIMISTA):\n"
            f"'''\n{argumento_bull}\n'''\n\n"
            f"Com base unicamente nos dados fornecidos, apresente a sua RÉPLICA CÉTICA (Bear), "
            f"rebatendo os pontos otimistas do Bull e reafirmando a necessidade de cautela/risco."
        )
    )

    # Invocação do LLM
    resposta = llm.invoke([mensagem_sistema, mensagem_usuario])

    # Retorna APENAS a chave atualizada para fusão limpa no estado global do LangGraph
    return {"replica_bear": resposta.content}
