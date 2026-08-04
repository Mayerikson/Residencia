from pathlib import Path

from pypdf import PdfReader


def carregar_pdfs(pasta_data: str = "data") -> list[dict]:
    """
    Lê todos os arquivos PDF da pasta data e retorna uma lista de trechos.
    Cada item contém o texto e metadados do arquivo de origem.
    """
    pasta = Path(pasta_data)
    if not pasta.exists():
        raise FileNotFoundError(f"A pasta '{pasta_data}' não existe.")

    pdfs = list(pasta.glob("*.pdf"))
    if not pdfs:
        raise FileNotFoundError(
            f"Nenhum PDF encontrado em '{pasta_data}'. Coloque pelo menos um arquivo .pdf lá."
        )

    documentos = []

    for caminho_pdf in pdfs:
        leitor = PdfReader(str(caminho_pdf))

        for numero_pagina, pagina in enumerate(leitor.pages, start=1):
            texto = pagina.extract_text() or ""
            texto = texto.strip()

            if not texto:
                continue

            documentos.append(
                {
                    "texto": texto,
                    "metadados": {
                        "arquivo": caminho_pdf.name,
                        "pagina": numero_pagina,
                    },
                }
            )

    if not documentos:
        raise ValueError("Os PDFs foram encontrados, mas nenhum texto pôde ser extraído.")

    return documentos


def dividir_em_chunks(documentos: list[dict], tamanho: int = 1000, sobreposicao: int = 200) -> list[dict]:
    """
    Divide textos longos em pedaços menores (chunks) para melhorar a busca semântica.
    """
    chunks = []

    for doc in documentos:
        texto = doc["texto"]
        inicio = 0

        while inicio < len(texto):
            fim = inicio + tamanho
            pedaco = texto[inicio:fim].strip()

            if pedaco:
                chunks.append(
                    {
                        "texto": pedaco,
                        "metadados": doc["metadados"],
                    }
                )

            inicio += tamanho - sobreposicao

    return chunks
