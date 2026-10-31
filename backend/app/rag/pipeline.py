from backend.app.rag.context_builder import build_context
from backend.app.rag.citation import create_citation


def prepare_rag_input(results: list) -> dict:
    context = build_context(results)

    citations = []

    for result in results:
        chunk = result["chunk"]
        citations.append(create_citation(chunk))

    return {
        "context": context,
        "citations": citations,
    }