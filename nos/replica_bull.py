"""
Módulo do Nó Réplica Bull (Réplica Otimista).
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


def no_replica_bull(estado: EstadoComite) -> dict:
    """
    Nó do LangGraph responsável pela RÉPLICA OTIMISTA (Bull).
    """
    ticker = estado.get("ticker", "Ativo")
    dados_mercado = estado.get("dados_mercado", "Sem dados disponíveis.")
    argumento_bear = estado.get("argumento_bear", "Sem argumento Bear inicial.")

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
    caminho_prompt = os.path.join("prompts", "replica_bull.md")
    conteudo_prompt_sistema = carregar_prompt(caminho_prompt)

    mensagem_sistema = SystemMessage(content=conteudo_prompt_sistema)

    mensagem_usuario = HumanMessage(
        content=(
            f"ATIVO ANALISADO: {ticker}\n\n"
            f"1. DADOS DE MERCADO E NOTÍCIAS:\n"
            f"'''\n{dados_mercado}\n'''\n\n"
            f"2. TESE INICIAL DO ANALISTA BEAR (CÉTICO/RISCO):\n"
            f"'''\n{argumento_bear}\n'''\n\n"
            f"Com base unicamente nos dados de mercado fornecidos, apresente a sua RÉPLICA OTIMISTA (Bull), "
            f"rebatendo os riscos apontados pelo Bear e reforçando por que a compra se justifica."
        )
    )

    # Invocação do LLM
    resposta = llm.invoke([mensagem_sistema, mensagem_usuario])

    # Retorna APENAS a chave atualizada para fusão limpa no estado global do LangGraph
    return {"replica_bull": resposta.content}
