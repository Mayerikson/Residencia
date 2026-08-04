"""
Script para indexar PDFs da pasta data no ChromaDB.

Uso:
    python ingest.py
"""

from src.pdf_loader import carregar_pdfs, dividir_em_chunks
from src.vectorstore import salvar_chunks_no_chroma


def main():
    print("Carregando PDFs da pasta data...")
    documentos = carregar_pdfs("data")

    print(f"Documentos carregados: {len(documentos)} página(s) com texto.")

    print("Dividindo textos em chunks...")
    chunks = dividir_em_chunks(documentos)
    print(f"Chunks gerados: {len(chunks)}")

    print("Gerando embeddings e salvando no ChromaDB...")
    total_salvo = salvar_chunks_no_chroma(chunks)

    print(f"Indexação concluída! {total_salvo} trecho(s) salvos em chroma_db/")


if __name__ == "__main__":
    main()
