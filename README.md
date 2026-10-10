# Synap

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white) ![LangChain](https://img.shields.io/badge/LangChain-1.x-1C3C3C?logo=langchain&logoColor=white) ![Cohere](https://img.shields.io/badge/Cohere-Embeddings-5F2EEA?logo=cohere&logoColor=white) ![Groq](https://img.shields.io/badge/Groq-LLM-FFD43B?logo=groq&logoColor=black) ![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)

![A bouncing ball animation](./asset/Project.gif)

Synap is a lightweight, end-to-end Retrieval-Augmented Generation (RAG) project designed to help you understand how document-based question answering is built from first principles. It ingests PDF documents, chunks them into semantically useful segments, embeds them into a vector space, retrieves the most relevant content for a user query, and sends the result to a large language model for grounded answers.

The project is intentionally code-first and educational: it strips the stack down to the core components that make RAG systems work while still being practical enough to use in a real workflow.

## Why this project

This repository is built for learners, builders, and practitioners who want a clear mental model of how a RAG pipeline works in practice.

- PDF ingestion and text extraction from real-world documents
- Chunking and knowledge-base construction from source material
- Embedding generation and semantic retrieval
- Prompt grounding to ensure answers are tied to the uploaded documents
- Chat memory to support follow-up questions in a conversation
- A usable Streamlit interface for interactive querying
- A clean modular structure so each step can be understood and extended

## What it does

The application accepts a folder of PDFs, extracts their text, creates a knowledge base, and retrieves the closest matching chunks for a user question. Those chunks are then injected into a system prompt and passed to a language model for answer generation.

In simple terms, the workflow is:

1. Load PDF files from the documents directory
2. Extract raw text from each page
3. Split the text into smaller chunks
4. Convert each chunk into embeddings
5. Store embeddings for retrieval
6. Encode the incoming question
7. Find the most relevant chunks
8. Feed those chunks into the prompt along with the user query
9. Generate a grounded answer
10. Keep chat history for conversational continuity

## Architecture

The project follows a modular pipeline structure, with responsibilities separated by task and domain.

```text
src/
├── app/
│   └── app.py                  # Streamlit UI entry point
├── components/
│   ├── __init__.py
│   ├── memory.py               # Conversation history helpers
│   ├── models.py               # LLM and embedding model setup
│   ├── parsers.py              # Output schema parser
│   ├── retrievar.py            # Semantic retrieval logic
│   └── templates.py            # Prompt templates and grounding instructions
├── rag_from_scratch/
│   ├── __init__.py
│   └── main.py                 # Runnable orchestration for the RAG chain
├── tasks/
│   ├── __init__.py
│   ├── document_loading.py     # PDF loading and knowledge base creation
│   ├── embedding.py            # Embedding generation and persistence
│   └── text_splitting.py       # Chunking logic
└── __init__.py

data/
├── docs/                       # Uploaded PDF documents
├── artifacts/
│   ├── chat_history.json
│   ├── chunks.json
│   └── knowledge_base.txt
└── embeddings/
    └── knowledge_base.json
```

## Core components

### 1. Document loading
The `DocumentLoader` class reads all `.pdf` files from a target folder, extracts text page by page, combines the results, and saves the merged knowledge base to `data/artifacts/knowledge_base.txt`.

### 2. Text splitting
The `TextSplitter` class breaks the document text into smaller chunks so the retrieval step can work with manageable segments instead of a single large blob of content.

### 3. Embeddings
The `Embedding` class creates embeddings for document chunks and queries using the configured embedding model. Embeddings are saved under `data/embeddings/knowledge_base.json` and reused when answering new questions.

### 4. Retrieval
The `Retrievar` class computes similarity between the query embedding and each document embedding. It ranks the results and returns the most relevant chunks, effectively powering the retrieval stage of RAG.

### 5. Prompt engineering and grounding
The project uses prompt templates with explicit assertions that the answer must be grounded in the retrieved documents. This is one of the most important parts of a strong RAG system: helping the model answer only from source context instead of hallucinating.

### 6. Chat memory
The `ChatHistory` helper stores and reloads prior messages so follow-up questions can reference earlier context in the same session.

### 7. Model configuration
`Models` wraps the selected LLM and embedding providers. The default setup uses Cohere embeddings and Groq-hosted LLM inference, while the code includes commented alternatives for Google Generative AI.

## Key technology stack

- Python 3.14+
- LangChain
- Cohere embeddings
- Groq chat models
- Streamlit
- PyPDF
- Python-dotenv
- JSON output parsing for structured responses

## Quick start

### Prerequisites

- Python 3.14 or newer
- `pip` or `uv`
- API keys for the model providers you want to use
- A folder of PDF documents to query

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd "RAG from scratch"
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

Using `pip`:

```bash
pip install -U pip
pip install -e .
```

Using `uv`:

```bash
uv sync
```

### 4. Configure environment variables

This project reads values from a `.env` file in the project root. Add the relevant keys before running the app.

```bash
GROQ_API_TOKEN=your_groq_api_key
COHERE_API_KEY=your_cohere_api_key
GOOGLE_API_KEY=your_google_api_key   # optional if you switch models
```

> The project already includes a `.env` file in the workspace, but you should replace its values with your own credentials before using it in a real environment.

## Run the application

### Streamlit app

Open the user-facing interface:

```bash
streamlit run src/app/app.py
```

This launches the chat interface where you can upload PDFs and ask questions about their content.

### Console runner

The project also includes a terminal-based RAG flow defined in `src/rag_from_scratch/main.py`:

```bash
python -m rag_from_scratch.main
```

Once running, it prompts for a query in the terminal and answers using the loaded knowledge base.

## Example usage

1. Place your PDF files in `data/docs/`
2. Launch the app with Streamlit
3. Upload the documents
4. Ask a question like:
   - "Summarize the key ideas in these documents"
   - "What are the main risks mentioned in the report?"
   - "Explain the section on architecture in simpler terms"
5. The app retrieves the most relevant chunks and generates a grounded answer

## Data flow

The project stores generated artifacts in a few predictable locations:

- `data/docs/` — source PDFs
- `data/artifacts/knowledge_base.txt` — combined extracted text
- `data/artifacts/chunks.json` — chunked text segments
- `data/artifacts/chat_history.json` — saved conversation history
- `data/embeddings/knowledge_base.json` — document embeddings

## Configuration notes

### Models
The `Models` class centralizes model selection. It currently uses:

- `CohereEmbeddings` for embeddings
- `ChatGroq` for generation

If you want to switch providers, update the model constructors inside `src/components/models.py`.

### Prompt behavior
The system prompt is intentionally strict:

- answers must be grounded in retrieved documents
- if no evidence is found, the model must say so clearly
- follow-up questions should respect conversational context

This makes the project a useful reference for building safer, more grounded AI systems.

## Project status

This project is a solid educational and prototype-level implementation of RAG. It is structured well for experimentation and learning and can be extended with:

- vector database backends such as FAISS or Chroma
- better retrieval ranking and reranking
- async workflows
- richer UI controls
- evaluation datasets and scoring metrics
- multi-index or hybrid search

## Roadmap

Planned areas of improvement include:

- Support for more file types beyond PDFs
- Vector database integration for larger corpora
- Better semantic chunking strategies
- Agent-style multi-step retrieval and reasoning
- Evaluation harness for answer quality and citation grounding
- Improved deployment packaging for local or cloud use

## Contributing

Contributions are welcome. If you want to improve the project:

1. Fork the repository
2. Create a feature branch
3. Make a focused change
4. Run your validation checks
5. Submit a pull request with a clear summary

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Author

Shriram Vibhute

## Summary

RAG from Scratch is a practical, educational implementation of document-grounded AI. It shows how a simple but effective retrieval pipeline can turn PDFs into a conversational knowledge system without hiding the mechanics behind a black box.

If you want to learn how RAG actually works, this repository is a great starting point because each part of the stack is visible, inspectable, and easy to modify.
