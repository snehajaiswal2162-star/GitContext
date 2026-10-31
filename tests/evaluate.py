import json
import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent)
)

from backend.app.ingestion.clone import clone_repository
from backend.app.ingestion.scanner import scan_repository
from backend.app.ingestion.filters import filter_files
from backend.app.ingestion.reader import read_file
from backend.app.ingestion.language import detect_language
from backend.app.ingestion.document import Document
from backend.app.chunking.chunker import chunk_document

from backend.app.embedding.embedder import Embedder
from backend.app.vector_store.qdrant_client import QdrantVectorStore
from backend.app.retrieval.hybrid import HybridRetriever
from backend.app.retrieval.reranker import Reranker


REPOSITORY_URL = (
    "https://github.com/"
    "snehajaiswal2162-star/"
    "Pizza-Slider"
)


def normalize(text):
    return (
        text.lower()
        .replace("`", "")
        .replace("'", "")
        .replace('"', "")
        .replace(" ", "")
    )


def answer_matches(question, retrieved_text):
    text = normalize(retrieved_text)

    if not text:
        return False

    # Test 1
    if "main pizza slider logic" in question.lower():
        return (
            "hero" in text
            and "hero.jsx" in text
        )

    # Test 2
    if "move function change the pizza rotation" in question.lower():
        return (
            "90" in text
            and "rotation" in text
            and (
                "direction" in text
                or "right" in text
                or "left" in text
            )
        )

    # Test 3
    if "state variable tracks the currently active pizza" in question.lower():
        return (
            "activeindex" in text
            or "activeindex" in text
        )

    # Test 4
    if "active pizza selected from the pizza array" in question.lower():
        return (
            "pizza[activeindex]" in text
            or (
                "pizza" in text
                and "activeindex" in text
            )
        )

    # Test 5
    if "left and right navigation" in question.lower():
        return (
            "move" in text
            and "left" in text
            and "right" in text
        )

    return False


def load_repository_chunks(repository_url):

    repository = (
        repository_url
        .rstrip("/")
        .split("/")[-1]
        .replace(".git", "")
    )

    repo_path = clone_repository(repository_url)

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

    return repository, chunks


def main():

    with open(
        "tests/evaluation_questions.json",
        "r",
        encoding="utf-8",
    ) as file:
        questions = json.load(file)

    total = len(questions)

    citation_correct = 0
    answer_correct = 0

    print("\nGitContext Retrieval Evaluation")
    print("=" * 60)

    print("\nLoading repository chunks...")

    repository, chunks = load_repository_chunks(
        REPOSITORY_URL
    )

    print(
        f"Loaded {len(chunks)} chunks "
        f"from {repository}"
    )

    print("\nLoading retrieval models...")

    embedder = Embedder()

    vector_store = QdrantVectorStore()

    hybrid_retriever = HybridRetriever(
        chunks=chunks,
        embedder=embedder,
        vector_store=vector_store,
        repository=repository,
    )

    reranker = Reranker()

    print("Retrieval models ready.")

    for number, item in enumerate(
        questions,
        start=1
    ):

        question = item["question"]
        expected_file = item["expected_file"]

        print(f"\nTest {number}")
        print(f"Question: {question}")

        # --------------------------------
        # Hybrid retrieval
        # --------------------------------

        results = hybrid_retriever.search(
            query=question,
            limit=5,
        )

        # --------------------------------
        # Reranking
        # --------------------------------

        results = reranker.rerank(
            query=question,
            results=results,
            limit=3,
        )

        # --------------------------------
        # Retrieved files
        # --------------------------------

        cited_files = []

        retrieved_text_parts = []

        for result in results:

            chunk = result["chunk"]

            cited_files.append(
                str(chunk.file_path)
            )

            retrieved_text_parts.append(
                f"""
File: {chunk.file_path}
Symbol: {chunk.symbol_name}
Lines: {chunk.start_line}-{chunk.end_line}

{chunk.content}
"""
            )

        retrieved_text = "\n".join(
            retrieved_text_parts
        )

        # --------------------------------
        # Citation evaluation
        # --------------------------------

        citation_found = any(
            expected_file.replace("\\", "/")
            == cited_file.replace("\\", "/")
            for cited_file in cited_files
        )

        if citation_found:
            citation_correct += 1

        # --------------------------------
        # Answer / retrieval evaluation
        # --------------------------------

        answer_found = answer_matches(
            question,
            retrieved_text,
        )

        if answer_found:
            answer_correct += 1

        # --------------------------------
        # Print result
        # --------------------------------

        print(
            "Citation: "
            f"{'PASS' if citation_found else 'FAIL'}"
        )

        print(
            "Retrieval: "
            f"{'PASS' if answer_found else 'FAIL'}"
        )

        print(
            f"Expected file: {expected_file}"
        )

        print(
            f"Retrieved files: {cited_files}"
        )

        if results:
            print("\nTop retrieved chunks:")

            for result in results:

                chunk = result["chunk"]

                print(
                    f"- {chunk.file_path} "
                    f"({chunk.symbol_name}) "
                    f"lines "
                    f"{chunk.start_line}-"
                    f"{chunk.end_line}"
                )

    # --------------------------------
    # Final metrics
    # --------------------------------

    citation_accuracy = (
        citation_correct / total
    ) * 100

    retrieval_accuracy = (
        answer_correct / total
    ) * 100

    print("\n" + "=" * 60)

    print(
        f"Citation Accuracy: "
        f"{citation_accuracy:.1f}%"
    )

    print(
        f"Retrieval Accuracy: "
        f"{retrieval_accuracy:.1f}%"
    )

    print(
        f"Passed Retrieval Tests: "
        f"{answer_correct}/{total}"
    )


if __name__ == "__main__":
    main()