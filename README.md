# Projeto RAG com Documentos PDF

Este projeto implementa um sistema de Geração Aumentada por Recuperação (RAG - Retrieval Augmented Generation) para interagir com documentos PDF. Ele permite que você faça perguntas sobre o conteúdo de seus PDFs e receba respostas baseadas exclusivamente nas informações contidas neles, com a capacidade de citar as fontes (arquivos e páginas).

## Visão Geral

O sistema funciona em duas etapas principais:

1.  **Indexação (Ingestão):** Processa documentos PDF de uma pasta designada, extrai seu texto, divide-o em pequenos trechos (chunks) e gera representações numéricas (embeddings) para cada trecho. Esses embeddings são armazenados em um banco de dados vetorial (ChromaDB), permitindo uma busca eficiente por similaridade semântica.
2.  **Consulta (QA):** Ao receber uma pergunta, o sistema busca os trechos mais relevantes no banco de dados vetorial. Esses trechos, juntamente com a pergunta original, são enviados a um modelo de linguagem grande (LLM) para gerar uma resposta concisa e fundamentada. A resposta inclui referências aos documentos e páginas de onde as informações foram extraídas.

## 🚀 Configuração e Execução

Para configurar e executar este projeto, siga os passos abaixo:

### 1. Clonar o Repositório

```bash
git clone https://github.com/Mayerikson/Residencia.git
cd Projeto-Residencia
```

### 2. Configurar Ambiente Virtual

É altamente recomendável usar um ambiente virtual para isolar as dependências do projeto.

```bash
# Criar ambiente virtual (venv)
python3 -m venv venv

# Ativar ambiente virtual (Linux/macOS)
source venv/bin/activate

# Ativar ambiente virtual (Windows)
virtual_env\Scripts\activate
```

### 3. Instalar Dependências

Com o ambiente virtual ativado, instale as bibliotecas necessárias:

```bash
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com suas chaves de API e configurações do modelo. **Nunca envie este arquivo para repositórios públicos.**

```
OPENAI_API_KEY=sua_chave_de_api_aqui
OPENAI_MODEL=gpt-4o-mini
EMBEDDING_MODEL=text-embedding-ada-002
```

*   **OPENAI_API_KEY:** Sua chave de API da OpenAI.
*   **OPENAI_MODEL:** O modelo da OpenAI a ser usado para geração de respostas (ex: `gpt-4o-mini`, `gpt-3.5-turbo`).
*   **EMBEDDING_MODEL:** O modelo da OpenAI a ser usado para gerar embeddings (ex: `text-embedding-ada-002`).

Adicione `.env` ao seu `.gitignore` para evitar que ele seja versionado.

### 5. Adicionar Documentos PDF

Coloque os arquivos PDF que você deseja indexar na pasta `data/`.

### 6. Indexar Documentos

Execute o script de ingestão para processar seus PDFs e construir o banco de dados vetorial:

```bash
python ingest.py
```

### 7. Iniciar a Aplicação Web

Execute a aplicação Streamlit para interagir com seus documentos:

```bash
streamlit run app.py
```

Abra seu navegador e acesse `http://localhost:8501` (ou a porta indicada pelo Streamlit).

### 🛑 Desativar Ambiente Virtual

Quando terminar de trabalhar, você pode desativar o ambiente virtual:

```bash
deactivate
```

## Estrutura do Projeto

```
.env.example
.gitignore
README.md
app.py
ingest.py
requirements.txt
data/
src/
├── __init__.py
├── pdf_loader.py
├── qa.py
└── vectorstore.py
```

## Contribuição

Sinta-se à vontade para contribuir com melhorias, correções de bugs ou novas funcionalidades. Abra uma *issue* ou envie um *pull request*.
