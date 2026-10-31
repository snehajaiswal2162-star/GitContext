from functools import lru_cache

from backend.app.rag.llm import GeminiLLM


@lru_cache(maxsize=1)
def get_llm():
    return GeminiLLM()


def generate_answer(
    question: str,
    context: str,
) -> str:

    prompt = f"""
You are GitContext, an AI assistant that answers questions
about software repositories.

Answer the user's question using ONLY the provided repository context.

If the context does not contain enough information to answer,
say that the information is not available in the retrieved context.

Do not invent files, functions, classes, or implementation details.

Repository context:
-------------------
{context}
-------------------

User question:
{question}

Give a clear and concise answer.
"""

    llm = get_llm()

    return llm.generate(prompt)