from functools import lru_cache
import time
import hashlib
import uuid

from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware

from backend.app.vector_store.qdrant_client import QdrantVectorStore
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


def generate_chunk_id(repository, file_path, chunk):
    unique_string = (
        f"{repository}:"
        f"{file_path}:"
        f"{chunk.chunk_type}:"
        f"{chunk.symbol_name}:"
        f"{chunk.start_line}:"
        f"{chunk.end_line}"
    )

    hash_value = hashlib.sha256(
        unique_string.encode("utf-8")
    ).hexdigest()

    return str(uuid.UUID(hash_value[:32]))

# ============================================================
# Cached components
# Heavy ML imports are intentionally lazy-loaded so that
# FastAPI can start without immediately loading PyTorch/models.
# ============================================================

@lru_cache(maxsize=1)
def get_embedder():
    from backend.app.embedding.embedder import Embedder
    return Embedder()


@lru_cache(maxsize=1)
def get_reranker():
    from backend.app.retrieval.reranker import Reranker
    return Reranker()


@lru_cache(maxsize=1)
def get_vector_store():
    store = QdrantVectorStore()
    store.ensure_collection()
    return store


# ============================================================
# FastAPI application
# ============================================================

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


# ============================================================
# Request and response models
# ============================================================

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


# ============================================================
# Health and welcome endpoints
# ============================================================

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


# ============================================================
# Repository indexing endpoint
# ============================================================

@app.post(
    "/repositories/index",
    response_model=IndexResponse,
)
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

    # --------------------------------------------------------
    # Check whether existing index is stale
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Full repository indexing
    # --------------------------------------------------------

    vector_store = get_vector_store()

    vector_store.delete_repository_chunks(
        repository=repository
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

    if not chunks:
        return IndexResponse(
            repository=repository,
            message="No supported repository content found.",
        )

    # Lazy-load the embedding model only when indexing is needed
    embedder = get_embedder()

    for chunk in chunks:

        vector = embedder.encode(
            chunk.content
        )

        point_id = generate_chunk_id(
        repository=repository,
        file_path=chunk.file_path,
        chunk=chunk,
    )


        vector_store.insert_chunk(
            point_id=point_id,
            vector=vector,
            chunk=chunk,
        )

    latest_commit = get_latest_commit(
        repo_path
    )

    save_index_state(
        repository=repository,
        commit_hash=latest_commit["commit_hash"],
    )

    return IndexResponse(
        repository=repository,
        message=(
            f"Repository indexed successfully. "
            f"{len(chunks)} chunks stored."
        ),
    )


# ============================================================
# Repository question endpoint
# ============================================================

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

    # --------------------------------------------------------
    # 1. Load repository chunks
    # --------------------------------------------------------

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
        f"Load repository chunks: "
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

    # --------------------------------------------------------
    # 2. Hybrid retrieval
    # --------------------------------------------------------

    start = time.time()

    # Heavy embedding model loads only when /ask is called
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
        f"Hybrid retrieval: "
        f"{time.time() - start:.2f}s"
    )

    if not results:
        return QuestionResponse(
            answer=(
                "No relevant repository context was found."
            ),
            citations=[],
        )

    # --------------------------------------------------------
    # 3. Reranking
    # --------------------------------------------------------

    start = time.time()

    # Heavy cross-encoder loads only when reranking is needed
    reranker = get_reranker()

    results = reranker.rerank(
        query=request.question,
        results=results,
        limit=3,
    )

    print(
        f"Reranking: "
        f"{time.time() - start:.2f}s"
    )

    if not results:
        return QuestionResponse(
            answer=(
                "No relevant repository context was found."
            ),
            citations=[],
        )

    # --------------------------------------------------------
    # 4. RAG context
    # --------------------------------------------------------

    start = time.time()

    rag_input = prepare_rag_input(
        results
    )

    print(
        f"RAG context: "
        f"{time.time() - start:.2f}s"
    )

    # --------------------------------------------------------
    # 5. Gemini answer generation
    # --------------------------------------------------------

    start = time.time()

    answer = generate_answer(
        question=request.question,
        context=rag_input["context"],
    )

    print(
        f"Gemini: "
        f"{time.time() - start:.2f}s"
    )

    print(
        f"TOTAL: "
        f"{time.time() - total_start:.2f}s"
    )

    return QuestionResponse(
        answer=answer,
        citations=rag_input["citations"],
    )