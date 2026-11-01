# GitContext — AI-Powered Codebase Intelligence & Developer Copilot

GitContext is an AI-powered codebase intelligence system that helps developers understand and explore GitHub repositories through natural-language questions.

Instead of manually searching through multiple files, developers can provide a GitHub repository URL and ask questions about its architecture, functions, backend components, indexing process, and implementation details.

GitContext retrieves relevant code snippets, uses an LLM to generate context-aware answers, and provides source citations so developers can trace answers back to the original files.

## Features

- **GitHub Repository Indexing:** Clone and index GitHub repositories.
- **Code Parsing and Chunking:** Break source files into meaningful chunks for better retrieval.
- **Semantic Search:** Retrieve code based on the meaning of a user's question.
- **BM25 Keyword Search:** Find relevant code using keyword-based retrieval.
- **Hybrid Retrieval:** Combine semantic and keyword search to improve retrieval relevance.
- **Vector Storage:** Store code embeddings and metadata in Qdrant.
- **AI-Powered Answers:** Generate natural-language answers using Google's Gemini models.
- **Source Citations:** Display relevant file names, symbols, and line ranges used to generate answers.
- **Incremental Reindexing:** Detect repository changes and update the index without always reprocessing the entire repository.
- **Developer-Friendly API:** Expose backend functionality through FastAPI.

## How It Works

1. **Repository Input:** The user provides a GitHub repository URL.
2. **Repository Ingestion:** GitContext retrieves the repository files and filters out unsupported files, secrets, and unnecessary directories.
3. **Code Chunking:** Source code is divided into smaller, meaningful chunks.
4. **Embedding Generation:** Gemini embedding models convert code chunks into vector representations.
5. **Vector Storage:** Embeddings and associated metadata are stored in Qdrant.
6. **Question Processing:** The user asks a natural-language question about the indexed repository.
7. **Hybrid Retrieval:** Semantic and BM25 search retrieve relevant code chunks.
8. **Answer Generation:** Gemini generates an answer using the retrieved context.
9. **Citations:** Relevant source files and line ranges are included with the answer.

## Technology Stack

| Component | Technology |
|---|---|
| Backend | Python, FastAPI |
| Frontend | HTML, CSS, JavaScript |
| LLM | Google Gemini |
| Embeddings | Gemini Embedding Model |
| Vector Database | Qdrant Cloud |
| Retrieval | Semantic Search, BM25, Hybrid Retrieval |
| Code Parsing | Tree-sitter |
| API Testing | Swagger UI |
| Version Control | Git and GitHub |
| Deployment | Render |

## Project Structure

```text
GitContext/
│
├── backend/
│   ├── app/
│   │   ├── ingestion/
│   │   ├── chunking/
│   │   ├── embedding/
│   │   ├── retrieval/
│   │   ├── vector_store/
│   │   └── rag/
│   │
│   ├── main.py
│   └── cli.py
│
├── frontend/
│   └── gitcontext-ui/
│       └── index.html
│
├── data/
│   └── repositories/
│
├── tests/
│
├── .env.example
├── .gitignore
├── docker-compose.yml
├── requirements.txt
└── README.md
```

*Note: The structure above shows the main project areas; individual files may vary.*

## Live Demo

- **Frontend:** https://gitcontext-frontend.onrender.com
- **Backend API:** https://gitcontexts.onrender.com
- **API Documentation:** https://gitcontexts.onrender.com/docs

## Environment Variables

Create a `.env` file in the project root and configure the following variables:

```env
GEMINI_API_KEY=your_gemini_api_key
QDRANT_URL=your_qdrant_cluster_url
QDRANT_API_KEY=your_qdrant_api_key
```

Never upload your `.env` file or expose API keys publicly.

## Installation and Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/snehajaiswal2162-star/GitContext.git
cd GitContext
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create your `.env` file using the variables listed above.

### 5. Start the FastAPI backend

```bash
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

### 6. Open API documentation

Visit:

```text
http://127.0.0.1:8000/docs
```

You can use the frontend by opening its `index.html` file in a browser. For local development, configure its API base URL to:

```javascript
const API_BASE = "http://127.0.0.1:8000";
```

For the deployed frontend, use the deployed backend URL instead.

## Example Questions

Once a repository has been indexed, you can ask questions such as:

- Explain the complete architecture of this repository.
- How does the FastAPI backend work?
- Explain the repository indexing process.
- How are code chunks stored in Qdrant?
- How does hybrid retrieval work?
- Explain the incremental reindexing process.
- What does a particular function do?
- Which files implement a specific feature?

## Future Improvements

- Improve response generation and retrieval speed.
- Optimize embedding generation and API requests.
- Improve retrieval ranking and answer relevance.
- Add support for larger repositories.
- Improve code dependency and relationship understanding.
- Add automated evaluation for retrieval quality and answer accuracy.

## Project Status

GitContext has a deployed frontend and backend and supports repository indexing, code retrieval, LLM-based question answering, and source citations.

## Author

**Sneha Jaiswal**

B.Tech — Artificial Intelligence and Data Science

GitHub: [snehajaiswal2162-star](https://github.com/snehajaiswal2162-star)

---

*GitContext — Understand your codebase by simply asking questions.*
