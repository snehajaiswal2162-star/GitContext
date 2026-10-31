from pathlib import Path

from backend.app.embedding.embedder import Embedder
from backend.app.retrieval.bm_25 import BM25Retriever
from backend.app.retrieval.hybrid import HybridRetriever
from backend.app.retrieval.reranker import Reranker
from backend.app.vector_store.qdrant_client import QdrantVectorStore

from backend.app.rag.pipeline import prepare_rag_input
from backend.app.rag.answer import generate_answer


print("\n" + "=" * 60)
print("END-TO-END RAG TEST")
print("=" * 60)


# --------------------------------------------------
# 1. Initialize components
# --------------------------------------------------

embedder = Embedder()
vector_store = QdrantVectorStore()


# --------------------------------------------------
# 2. Load chunks for BM25
# --------------------------------------------------


# 2. Load chunks for BM25

from backend.app.ingestion.scanner import scan_repository
from backend.app.ingestion.filters import filter_files
from backend.app.ingestion.reader import read_file
from backend.app.ingestion.language import detect_language
from backend.app.ingestion.document import Document
from backend.app.chunking.chunker import chunk_document

repo_path = Path("data/repositories/Hello-World")

all_files = scan_repository(repo_path)
filtered_files = filter_files(all_files)

print(f"\nFiles found: {len(all_files)}")
print(f"Files after filtering: {len(filtered_files)}")

chunks = []

for path in filtered_files:
    content = read_file(path)

    if not content.strip():
        continue

    document = Document(
        repository="Hello-World",
        file_path=path.relative_to(repo_path),
        content=content,
        language=detect_language(path),
    )

    chunks.extend(chunk_document(document))

print(f"\nChunks loaded: {len(chunks)}")
for chunk in chunks:
    print(f"{chunk.file_path} | {chunk.symbol_name}")



# --------------------------------------------------
# 3. Hybrid retrieval
# --------------------------------------------------

hybrid = HybridRetriever(
    chunks=chunks,
    embedder=embedder,
    vector_store=vector_store,
    repository="Hello-World",

)

question = "Which database does this project use?"

hybrid_results = hybrid.search(
    query=question,
    limit=5,
)


print("\nHybrid results:")

for result in hybrid_results:
    print(
        result["chunk"].file_path,
        result["hybrid_score"],
    )


# --------------------------------------------------
# 4. Reranking
# --------------------------------------------------

reranker = Reranker()

reranked_results = reranker.rerank(
    query=question,
    results=hybrid_results,
    limit=3,
)


print("\nReranked results:")

for result in reranked_results:

    chunk = result["chunk"]

    print(
        chunk.file_path,
        chunk.symbol_name,
        result["rerank_score"],
    )


# --------------------------------------------------
# 5. Prepare RAG input
# --------------------------------------------------

rag_input = prepare_rag_input(
    results=reranked_results,
)


print("\nRAG context:")
print(rag_input["context"])


print("\nCitations:")

for citation in rag_input["citations"]:
    print(citation)


# --------------------------------------------------
# 6. Generate grounded answer
# --------------------------------------------------

answer = generate_answer(
    question=question,
    context=rag_input["context"],
)


print("\nGenerated answer:")
print(answer)


print("\n" + "=" * 60)
print("END-TO-END RAG TEST COMPLETE")
print("=" * 60)


from backend.app.ingestion.scanner import scan_repository
from backend.app.ingestion.filters import filter_files
from backend.app.ingestion.reader import read_file
from backend.app.ingestion.language import detect_language
from backend.app.ingestion.document import Document
from backend.app.chunking.chunker import chunk_document


repo_path = Path("data/repositories/Hello-World")

# Scan repository
all_files = scan_repository(repo_path)

# Apply GitContext's real filtering rules
filtered_files = filter_files(all_files)

print(f"\nFiles found: {len(all_files)}")
print(f"Files after filtering: {len(filtered_files)}")


# Create documents
documents = []

for path in filtered_files:

    content = read_file(path)

    if not content.strip():
        continue

    document = Document(
        repository="Hello-World",
        file_path=path.relative_to(repo_path),
        content=content,
        language=detect_language(path),
    )

    documents.append(document)


# Create chunks
chunks = []

for document in documents:
    chunks.extend(chunk_document(document))