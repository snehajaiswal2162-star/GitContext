from sentence_transformers import CrossEncoder


class Reranker:

    def __init__(
        self,
        model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2",
    ):
        self.model = CrossEncoder(model_name)

    def rerank(
        self,
        query: str,
        results: list,
        limit: int = 3,
    ):
        pairs = []

        for result in results:
            chunk = result["chunk"]

            # Limit the amount of code sent to the reranker.
            content = chunk.content[:4000]

            pairs.append(
                (
                    query,
                    content,
                )
            )

        scores = self.model.predict(
            pairs,
            batch_size=5,
            show_progress_bar=False,
        )

        reranked_results = []

        for result, score in zip(results, scores):

            reranked_result = result.copy()

            reranked_result["rerank_score"] = float(score)

            reranked_results.append(
                reranked_result
            )

        reranked_results.sort(
            key=lambda result: result["rerank_score"],
            reverse=True,
        )

        return reranked_results[:limit]