import os

from dotenv import load_dotenv
from qdrant_client import QdrantClient

from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
)

load_dotenv()


class QdrantVectorStore:

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6333,
    ):
        qdrant_url = os.getenv("QDRANT_URL")
        qdrant_api_key = os.getenv("QDRANT_API_KEY")

        # Use Qdrant Cloud when credentials are available.
        if qdrant_url and qdrant_api_key:
            self.client = QdrantClient(
                url=qdrant_url,
                api_key=qdrant_api_key,
            )
        else:
            # Fall back to local Qdrant for development.
            self.client = QdrantClient(
                host=host,
                port=port,
            )

    def test_connection(self):
        return self.client.get_collections()

    def create_collection(
        self,
        collection_name: str = "gitcontext_chunks",
    ):
        self.client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE,
            ),
        )

    def ensure_collection(
        self,
        collection_name: str = "gitcontext_chunks",
    ):
        """
        Create the collection only if it does not already exist.
        """
        if not self.client.collection_exists(collection_name):
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(
                    size=384,
                    distance=Distance.COSINE,
                ),
            )

            print(
                f"Created Qdrant collection: {collection_name}"
            )
        else:
            print(
                f"Qdrant collection already exists: {collection_name}"
            )

    def insert_chunk(
        self,
        point_id: str,
        vector: list[float],
        chunk,
    ):
        point = PointStruct(
            id=point_id,
            vector=vector,
            payload={
                "repository": chunk.repository,
                "file_path": str(chunk.file_path),
                "language": chunk.language,
                "chunk_type": chunk.chunk_type,
                "symbol_name": chunk.symbol_name,
                "start_line": chunk.start_line,
                "end_line": chunk.end_line,
                "content": chunk.content,
            },
        )

        self.client.upsert(
            collection_name="gitcontext_chunks",
            points=[point],
        )

    def get_chunk(self, point_id: int):
        return self.client.retrieve(
            collection_name="gitcontext_chunks",
            ids=[point_id],
            with_vectors=True,
        )

    def search(
        self,
        query_vector: list[float],
        limit: int = 3,
        repository: str | None = None,
    ):
        query_filter = None

        if repository:
            query_filter = Filter(
                must=[
                    FieldCondition(
                        key="repository",
                        match=MatchValue(
                            value=repository,
                        ),
                    )
                ]
            )

        return self.client.query_points(
            collection_name="gitcontext_chunks",
            query=query_vector,
            query_filter=query_filter,
            limit=limit,
            with_payload=True,
        )

    def delete_file_chunks(
        self,
        repository: str,
        file_path: str,
    ):
        self.client.delete(
            collection_name="gitcontext_chunks",
            points_selector=Filter(
                must=[
                    FieldCondition(
                        key="repository",
                        match=MatchValue(
                            value=repository,
                        ),
                    ),
                    FieldCondition(
                        key="file_path",
                        match=MatchValue(
                            value=file_path,
                        ),
                    ),
                ]
            ),
        )

    def delete_repository_chunks(
        self,
        repository: str,
    ):
        self.client.delete(
            collection_name="gitcontext_chunks",
            points_selector=Filter(
                must=[
                    FieldCondition(
                        key="repository",
                        match=MatchValue(
                            value=repository,
                        ),
                    ),
                ]
            ),
        )