"""
Módulo dos Nós Juízes Especializados por Perfil de Risco (Conservador, Moderado, Agressivo).
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


def _invocar_juiz(estado: EstadoComite, arquivo_prompt: str) -> str:
    """
    Função utilitária interna para montar o contexto comum do debate e invocar o LLM.
    """
    ticker = estado.get("ticker", "Ativo")
    dados_mercado = estado.get("dados_mercado", "Sem dados de mercado.")
    dados_estatisticos = estado.get("dados_estatisticos", "Sem dados estatísticos.")
    argumento_bull = estado.get("argumento_bull", "Sem argumento Bull.")
    argumento_bear = estado.get("argumento_bear", "Sem argumento Bear.")
    replica_bull = estado.get("replica_bull", "Sem réplica Bull.")
    replica_bear = estado.get("replica_bear", "Sem réplica Bear.")

    # Configurações do .env
    modelo_nome = os.getenv("OPENAI_MODEL")
    temperatura = float(os.getenv("TEMPERATURE", "0.2"))
    api_key = os.getenv("OPENAI_API_KEY")

    llm = ChatOpenAI(
        model=modelo_nome,
        temperature=temperatura,
        api_key=api_key,
        http_client=httpx.Client()
    )

    caminho_prompt = os.path.join("prompts", arquivo_prompt)
    conteudo_prompt_sistema = carregar_prompt(caminho_prompt)

    mensagem_sistema = SystemMessage(content=conteudo_prompt_sistema)
    mensagem_usuario = HumanMessage(
        content=(
            f"ATIVO ANALISADO: {ticker}\n\n"
            f"1. DADOS DE MERCADO E NOTÍCIAS (QUALITATIVO/QUANTITATIVO BRUTO):\n"
            f"'''\n{dados_mercado}\n'''\n\n"
            f"2. ANÁLISE ESTATÍSTICA QUANTITATIVA IMPARCIAL:\n"
            f"'''\n{dados_estatisticos}\n'''\n\n"
            f"3. TESE INICIAL BULL (OTIMISTA):\n"
            f"'''\n{argumento_bull}\n'''\n\n"
            f"4. TESE INICIAL BEAR (CÉTICO/RISCO):\n"
            f"'''\n{argumento_bear}\n'''\n\n"
            f"5. RÉPLICA BULL (REBATENDO O BEAR):\n"
            f"'''\n{replica_bull}\n'''\n\n"
            f"6. RÉPLICA BEAR (REBATENDO O BULL):\n"
            f"'''\n{replica_bear}\n'''\n\n"
            f"Com base unicamente nesse debate completo e nos dados quantitativos, avalie sob a ótica "
            f"do seu perfil de risco e emita a sua recomendação (Comprar, Aguardar ou Evitar) e nível de confiança."
        )
    )

    resposta = llm.invoke([mensagem_sistema, mensagem_usuario])
    return resposta.content


def no_juiz_conservador(estado: EstadoComite) -> dict:
    """
    Nó do LangGraph para o Juiz CONSERVADOR.
    Prioriza preservação de capital e aversão a risco.
    Retorna APENAS {"decisao_conservador": texto}.
    """
    resultado_texto = _invocar_juiz(estado, "juiz_conservador.md")
    return {"decisao_conservador": resultado_texto}


def no_juiz_moderado(estado: EstadoComite) -> dict:
    """
    Nó do LangGraph para o Juiz MODERADO.
    Busca equilíbrio neutro entre risco e retorno.
    Retorna APENAS {"decisao_moderado": texto}.
    """
    resultado_texto = _invocar_juiz(estado, "juiz_moderado.md")
    return {"decisao_moderado": resultado_texto}


def no_juiz_agressivo(estado: EstadoComite) -> dict:
    """
    Nó do LangGraph para o Juiz AGRESSIVO.
    Prioriza potencial de retorno e captura de alta.
    Retorna APENAS {"decisao_agressivo": texto}.
    """
    resultado_texto = _invocar_juiz(estado, "juiz_agressivo.md")
    return {"decisao_agressivo": resultado_texto}
