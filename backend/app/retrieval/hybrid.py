from backend.app.retrieval.bm_25 import BM25Retriever


class HybridRetriever:

    def __init__(
        self,
        chunks,
        embedder,
        vector_store,
        repository: str | None = None,
    ):
        self.chunks = chunks
        self.embedder = embedder
        self.vector_store = vector_store
        self.repository = repository
        self.bm25 = BM25Retriever(chunks)

    def chunk_key(self, chunk):
        return (
            f"{chunk.file_path}:"
            f"{chunk.symbol_name}:"
            f"{chunk.start_line}:"
            f"{chunk.end_line}"
        )

    def normalize_scores(self, scores):
        if not scores:
            return {}

        max_score = max(scores.values())

        if max_score <= 0:
            return {
                key: 0.0
                for key in scores
            }

        return {
            key: value / max_score
            for key, value in scores.items()
        }

    def search(
        self,
        query: str,
        limit: int = 3,
    ):
        query_vector = self.embedder.encode(query)

        semantic_results = self.vector_store.search(
            query_vector=query_vector,
            limit=len(self.chunks),
            repository=self.repository,
        )

        bm25_results = self.bm25.search(
            query=query,
            limit=len(self.chunks),
        )

        semantic_scores = {}

        for result in semantic_results.points:

            payload = result.payload

            key = (
                f"{payload['file_path']}:"
                f"{payload['symbol_name']}:"
                f"{payload['start_line']}:"
                f"{payload['end_line']}"
            )

            semantic_scores[key] = result.score

        bm25_scores = {}

        for result in bm25_results:

            chunk = result["chunk"]

            key = self.chunk_key(chunk)

            bm25_scores[key] = result["score"]

        normalized_semantic_scores = (
            self.normalize_scores(
                semantic_scores
            )
        )

        normalized_bm25_scores = (
            self.normalize_scores(
                bm25_scores
            )
        )

        combined_results = []

        for chunk in self.chunks:

            key = self.chunk_key(chunk)

            semantic_score = semantic_scores.get(
                key,
                0.0,
            )

            bm25_score = bm25_scores.get(
                key,
                0.0,
            )

            normalized_semantic = (
                normalized_semantic_scores.get(
                    key,
                    0.0,
                )
            )

            normalized_bm25 = (
                normalized_bm25_scores.get(
                    key,
                    0.0,
                )
            )

            hybrid_score = (
                0.7 * normalized_semantic
                + 0.3 * normalized_bm25
            )

            combined_results.append(
                {
                    "chunk": chunk,
                    "semantic_score": semantic_score,
                    "bm25_score": bm25_score,
                    "normalized_semantic": normalized_semantic,
                    "normalized_bm25": normalized_bm25,
                    "hybrid_score": hybrid_score,
                }
            )

        combined_results.sort(
            key=lambda result: result["hybrid_score"],
            reverse=True,
        )

        return combined_results[:limit]