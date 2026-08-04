import os
from pathlib import Path

import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from dotenv import load_dotenv

load_dotenv()

NOME_COLECAO = "documentos_rag"
PASTA_CHROMA = "chroma_db"


def criar_embedding_function() -> OpenAIEmbeddingFunction:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY não encontrada. Configure o arquivo .env.")

    modelo = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

    return OpenAIEmbeddingFunction(
        api_key=api_key,
        model_name=modelo,
    )


def obter_cliente_chroma() -> chromadb.PersistentClient:
    Path(PASTA_CHROMA).mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(path=PASTA_CHROMA)


def obter_ou_criar_colecao():
    cliente = obter_cliente_chroma()
    embedding_function = criar_embedding_function()

    return cliente.get_or_create_collection(
        name=NOME_COLECAO,
        embedding_function=embedding_function,
    )


def salvar_chunks_no_chroma(chunks: list[dict]) -> int:
    """
    Gera embeddings e salva os chunks no ChromaDB.
    Retorna a quantidade de trechos salvos.
    """
    colecao = obter_ou_criar_colecao()

    ids = []
    documentos = []
    metadados = []

    for indice, chunk in enumerate(chunks):
        ids.append(f"chunk_{indice}")
        documentos.append(chunk["texto"])
        metadados.append(chunk["metadados"])

    colecao.upsert(
        ids=ids,
        documents=documentos,
        metadados=metadados,
    )

    return len(chunks)


def buscar_contexto(pergunta: str, quantidade: int = 4) -> list[dict]:
    """
    Busca no ChromaDB os trechos mais relevantes para a pergunta.
    """
    colecao = obter_ou_criar_colecao()

    resultado = colecao.query(
        query_texts=[pergunta],
        n_results=quantidade,
    )

    trechos = []

    for documento, metadado in zip(resultado["documents"][0], resultado["metadatas"][0]):
        trechos.append(
            {
                "texto": documento,
                "metadados": metadado,
            }
        )

    return trechos
