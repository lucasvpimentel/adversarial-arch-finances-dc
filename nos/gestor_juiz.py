"""
Módulo do Nó Gestor / Juiz (Decisor Final do Comitê).
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


def no_gestor_juiz(estado: EstadoComite) -> dict:
    """
    Nó do LangGraph responsável por tomar a DECISÃO FINAL (Gestor/Juiz).
    """
    ticker = estado.get("ticker", "Ativo")
    dados_mercado = estado.get("dados_mercado", "Sem dados disponíveis.")
    argumento_bull = estado.get("argumento_bull", "Sem argumento Bull inicial.")
    argumento_bear = estado.get("argumento_bear", "Sem argumento Bear inicial.")
    replica_bull = estado.get("replica_bull", "Sem réplica Bull fornecida.")
    replica_bear = estado.get("replica_bear", "Sem réplica Bear fornecida.")

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
    caminho_prompt = os.path.join("prompts", "gestor_juiz.md")
    conteudo_prompt_sistema = carregar_prompt(caminho_prompt)

    mensagem_sistema = SystemMessage(content=conteudo_prompt_sistema)

    mensagem_usuario = HumanMessage(
        content=(
            f"ATIVO ANALISADO: {ticker}\n\n"
            f"1. DADOS DE MERCADO E NOTÍCIAS:\n"
            f"'''\n{dados_mercado}\n'''\n\n"
            f"2. TESE INICIAL BULL (OTIMISTA):\n"
            f"'''\n{argumento_bull}\n'''\n\n"
            f"3. TESE INICIAL BEAR (CÉTICO/RISCO):\n"
            f"'''\n{argumento_bear}\n'''\n\n"
            f"4. RÉPLICA BULL (REBATENDO O BEAR):\n"
            f"'''\n{replica_bull}\n'''\n\n"
            f"5. RÉPLICA BEAR (REBATENDO O BULL):\n"
            f"'''\n{replica_bear}\n'''\n\n"
            f"Com base unicamente nessas informações do debate completo, aja como o Gestor do Comitê, "
            f"analise imparcialmente ambos os lados e emita o seu relatório conclusivo com a "
            f"decisão (Comprar, Aguardar ou Evitar) e o nível de confiança (Baixo, Médio ou Alto)."
        )
    )

    # Invocação do LLM
    resposta = llm.invoke([mensagem_sistema, mensagem_usuario])

    # Retorna APENAS a chave atualizada para fusão limpa no estado global do LangGraph
    return {"decisao_final": resposta.content}
