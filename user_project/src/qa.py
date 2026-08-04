import os

from dotenv import load_dotenv
from openai import OpenAI

from src.vectorstore import buscar_contexto

load_dotenv()


def montar_prompt(pergunta: str, trechos: list[dict]) -> str:
    contexto = "\n\n".join(
        f"[Fonte: {trecho['metadados'].get('arquivo', 'desconhecido')} | "
        f"Página: {trecho['metadados'].get('pagina', '?')}]\n"
        f"{trecho['texto']}"
        for trecho in trechos
    )

    return f"""Você é um assistente que responde perguntas com base apenas no contexto fornecido.

Contexto:
{contexto}

Pergunta:
{pergunta}

Instruções:
- Responda em português.
- Use somente as informações do contexto.
- Se a resposta não estiver no contexto, diga claramente que não encontrou a informação nos documentos.
- Quando possível, cite o arquivo e a página de origem.
"""


def responder_pergunta(pergunta: str, quantidade_trechos: int = 4) -> dict:
    """
    Faz a pergunta ao sistema RAG:
    1. Busca trechos relevantes no ChromaDB
    2. Envia contexto + pergunta para a OpenAI
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY não encontrada. Configure o arquivo .env.")

    modelo = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    client = OpenAI(api_key=api_key)

    trechos = buscar_contexto(pergunta, quantidade=quantidade_trechos)

    if not trechos:
        return {
            "resposta": "Não encontrei documentos indexados. Execute primeiro o script ingest.py.",
            "fontes": [],
        }

    prompt = montar_prompt(pergunta, trechos)

    resposta = client.chat.completions.create(
        model=modelo,
        messages=[
            {
                "role": "system",
                "content": "Você responde perguntas com base em documentos PDF indexados.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    return {
        "resposta": resposta.choices[0].message.content,
        "fontes": trechos,
    }
