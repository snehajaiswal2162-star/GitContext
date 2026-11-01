
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
            f"{str(chunk.file_path)}:"
            f"{chunk.symbol_name}:"
            f"{chunk.start_line}:"
            f"{chunk.end_line}"
        )

    def search(self, query: str, limit: int = 3):
        if not self.chunks:
            return []

        candidate_limit = min(30, len(self.chunks))

        query_vector = self.embedder.encode(query)

        semantic_results = self.vector_store.search(
            query_vector=query_vector,
            limit=candidate_limit,
            repository=self.repository,
        )

        bm25_results = self.bm25.search(
            query=query,
            limit=candidate_limit,
        )

        chunks_by_key = {
            self.chunk_key(chunk): chunk
            for chunk in self.chunks
        }

        scores = {}

        # Semantic ranking contribution.
        for rank, point in enumerate(semantic_results.points, start=1):
            payload = point.payload or {}

            key = (
                f"{str(payload.get('file_path', ''))}:"
                f"{payload.get('symbol_name', '')}:"
                f"{payload.get('start_line', '')}:"
                f"{payload.get('end_line', '')}"
            )

            if key not in chunks_by_key:
                continue

            scores.setdefault(key, {
                "semantic_score": float(point.score),
                "bm25_score": 0.0,
                "hybrid_score": 0.0,
            })

            scores[key]["hybrid_score"] += 1.0 / (60 + rank)

        # BM25 ranking contribution.
        for rank, result in enumerate(bm25_results, start=1):
            chunk = result["chunk"]
            key = self.chunk_key(chunk)

            if key not in chunks_by_key:
                continue

            scores.setdefault(key, {
                "semantic_score": 0.0,
                "bm25_score": 0.0,
                "hybrid_score": 0.0,
            })

            scores[key]["bm25_score"] = float(result["score"])
            scores[key]["hybrid_score"] += 1.0 / (60 + rank)

        combined_results = []

        for key, score_data in scores.items():
            combined_results.append({
                "chunk": chunks_by_key[key],
                **score_data,
            })

        combined_results.sort(
            key=lambda item: item["hybrid_score"],
            reverse=True,
        )

        return combined_results[:limit]
