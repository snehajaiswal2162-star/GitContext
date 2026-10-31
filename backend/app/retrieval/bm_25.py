import re

from rank_bm25 import BM25Okapi


def tokenize(text: str) -> list[str]:
    text = re.sub(
        r"([a-z0-9])([A-Z])",
        r"\1 \2",
        text,
    )

    text = text.replace("_", " ")

    return re.findall(
        r"[a-zA-Z0-9]+",
        text.lower(),
    )


class BM25Retriever:

    def __init__(self, chunks):

        self.chunks = chunks

        documents = [
                f"{chunk.symbol_name} "
                f"{chunk.file_path} "
                f"{chunk.chunk_type} "
                f"{chunk.content}"
                for chunk in chunks
            ]

        tokenized_documents = [
            tokenize(document)
            for document in documents
        ]

        self.bm25 = BM25Okapi(
            tokenized_documents
        )

    def search(
        self,
        query: str,
        limit: int = 3,
    ):

        tokenized_query = tokenize(query)

        scores = self.bm25.get_scores(
            tokenized_query
        )

        ranked_indices = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True,
        )

        results = []

        for index in ranked_indices[:limit]:

            results.append(
                {
                    "chunk": self.chunks[index],
                    "score": scores[index],
                }
            )

        return results