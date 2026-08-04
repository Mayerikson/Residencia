import streamlit as st

from src.qa import responder_pergunta

st.set_page_config(
    page_title="Assistente RAG com PDFs",
    page_icon="📄",
    layout="wide",
)

st.title("📄 Assistente RAG com PDFs")
st.markdown(
    """
    Faça perguntas sobre os documentos que você indexou na pasta `data/`.

    **Antes de usar:**
    1. Coloque um PDF em `data/`
    2. Execute `python ingest.py`
    3. Volte aqui e faça sua pergunta
    """
)

with st.sidebar:
    st.header("Configurações")
    quantidade_trechos = st.slider(
        "Quantidade de trechos de contexto",
        min_value=1,
        max_value=8,
        value=4,
    )

pergunta = st.text_area(
    "Digite sua pergunta:",
    placeholder="Exemplo: Qual é o tema principal do documento?",
    height=120,
)

if st.button("Perguntar", type="primary"):
    if not pergunta.strip():
        st.warning("Digite uma pergunta antes de continuar.")
    else:
        with st.spinner("Buscando nos documentos e gerando resposta..."):
            try:
                resultado = responder_pergunta(
                    pergunta=pergunta.strip(),
                    quantidade_trechos=quantidade_trechos,
                )

                st.subheader("Resposta")
                st.write(resultado["resposta"])

                if resultado["fontes"]:
                    st.subheader("Fontes usadas")
                    for indice, fonte in enumerate(resultado["fontes"], start=1):
                        metadados = fonte["metadados"]
                        st.markdown(
                            f"**Trecho {indice}** — "
                            f"`{metadados.get('arquivo', 'desconhecido')}` "
                            f"(página {metadados.get('pagina', '?')})"
                        )
                        st.caption(fonte["texto"][:400] + ("..." if len(fonte["texto"]) > 400 else ""))

            except Exception as erro:
                st.error(f"Erro ao processar a pergunta: {erro}")
