
from functools import lru_cache
import time

from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware

from backend.app.embedding.embedder import Embedder
from backend.app.vector_store.qdrant_client import QdrantVectorStore
from backend.app.retrieval.reranker import Reranker
from backend.app.retrieval.hybrid import HybridRetriever
from backend.app.rag.pipeline import prepare_rag_input
from backend.app.rag.answer import generate_answer

from backend.app.ingestion.scanner import scan_repository
from backend.app.ingestion.filters import filter_files
from backend.app.ingestion.reader import read_file
from backend.app.ingestion.language import detect_language
from backend.app.ingestion.document import Document
from backend.app.chunking.chunker import chunk_document
from backend.app.ingestion.clone import clone_repository

from backend.app.ingestion.git_history import get_latest_commit
from backend.app.ingestion.index_state import save_index_state


# Cached components

@lru_cache(maxsize=1)
def get_embedder():
    return Embedder()


@lru_cache(maxsize=1)
def get_reranker():
    return Reranker()


@lru_cache(maxsize=1)
def get_vector_store():
    return QdrantVectorStore()


# FastAPI application

app = FastAPI(
    title="GitContext API",
    description="Codebase intelligence and developer copilot",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request and response models

class QuestionRequest(BaseModel):
    question: str = Field(
        min_length=3,
        description="Question about the repository",
    )

    repository_url: str = Field(
        min_length=1,
        description="GitHub repository URL",
    )


class IndexRequest(BaseModel):
    repository_url: str = Field(
        min_length=1,
        description="GitHub repository URL",
    )


class Citation(BaseModel):
    repository: str
    file_path: str
    symbol_name: str
    start_line: int
    end_line: int


class QuestionResponse(BaseModel):
    answer: str
    citations: list[Citation]


class IndexResponse(BaseModel):
    repository: str
    message: str


# Health and welcome endpoints

@app.get("/")
def root():
    return {
        "message": "Welcome to GitContext API",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
    }


# Repository indexing endpoint

@app.post(
    "/repositories/index",
    response_model=IndexResponse,
)
@app.post("/repositories/index")
def index_repository(request: IndexRequest):

    repo_path = clone_repository(
        request.repository_url
    )

    repository = repo_path.name

    from backend.app.ingestion.index_state import (
        get_indexed_commit_hash,
    )
    from backend.app.ingestion.reindex import (
        update_index_if_stale,
    )

    indexed_commit = get_indexed_commit_hash(
        repository
    )

    if indexed_commit is not None:
        latest_commit = get_latest_commit(
            repo_path
        )

        if (
            indexed_commit
            == latest_commit["commit_hash"]
        ):
            return IndexResponse(
                repository=repository,
                message=(
                    "Repository is already up to date."
                ),
            )

        update_index_if_stale(
            repo_path=repo_path,
            repository=repository,
        )

        return IndexResponse(
            repository=repository,
            message=(
                "Repository was stale. "
                "Incremental re-index completed."
            ),
        )

    vector_store = get_vector_store()

    vector_store.delete_repository_chunks(
        repository=repository
    )


# Repository question endpoint

@app.post(
    "/ask",
    response_model=QuestionResponse,
)
def ask_question(request: QuestionRequest):

    repository = (
        request.repository_url
        .rstrip("/")
        .split("/")[-1]
        .replace(".git", "")
    )

    total_start = time.time()

    # --------------------------------
    # 1. Load indexed repository chunks
    # --------------------------------

    start = time.time()

    repo_path = clone_repository(
        request.repository_url
    )

    files = filter_files(
        scan_repository(repo_path)
    )

    chunks = []

    for path in files:

        content = read_file(path)

        if not content.strip():
            continue

        document = Document(
            repository=repository,
            file_path=path.relative_to(repo_path),
            content=content,
            language=detect_language(path),
        )

        chunks.extend(
            chunk_document(document)
        )

    print(
        f"⏱ Load repository chunks: "
        f"{time.time() - start:.2f}s"
    )

    if not chunks:
        return QuestionResponse(
            answer=(
                "No indexed repository content was found. "
                "Please index the repository first."
            ),
            citations=[],
        )

    # --------------------------------
    # 2. Hybrid retrieval
    # --------------------------------

    start = time.time()

    embedder = get_embedder()
    vector_store = get_vector_store()

    hybrid_retriever = HybridRetriever(
        chunks=chunks,
        embedder=embedder,
        vector_store=vector_store,
        repository=repository,
    )

    results = hybrid_retriever.search(
        query=request.question,
        limit=5,
    )

    print(
        f"⏱ Hybrid retrieval: "
        f"{time.time() - start:.2f}s"
    )

    if not results:
        return QuestionResponse(
            answer="No relevant repository context was found.",
            citations=[],
        )

    # --------------------------------
    # 3. Reranking
    # --------------------------------

    start = time.time()

    reranker = get_reranker()

    results = reranker.rerank(
        query=request.question,
        results=results,
        limit=3,
    )

    print(
        f"⏱ Reranking: "
        f"{time.time() - start:.2f}s"
    )

    if not results:
        return QuestionResponse(
            answer="No relevant repository context was found.",
            citations=[],
        )

    # --------------------------------
    # 4. RAG context
    # --------------------------------

    start = time.time()

    rag_input = prepare_rag_input(results)

    print(
        f"⏱ RAG context: "
        f"{time.time() - start:.2f}s"
    )

    # --------------------------------
    # 5. Gemini
    # --------------------------------

    start = time.time()

    answer = generate_answer(
        question=request.question,
        context=rag_input["context"],
    )

    print(
        f"⏱ Gemini: "
        f"{time.time() - start:.2f}s"
    )

    print(
        f"⏱ TOTAL: "
        f"{time.time() - total_start:.2f}s"
    )

    return QuestionResponse(
        answer=answer,
        citations=rag_input["citations"],
    )
