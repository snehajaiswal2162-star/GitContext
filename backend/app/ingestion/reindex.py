from pathlib import Path
import hashlib
import uuid

from backend.app.ingestion.reader import read_file
from backend.app.ingestion.language import detect_language
from backend.app.ingestion.document import Document
from backend.app.ingestion.filters import (
    is_secret_file,
    is_supported_file,
)
from backend.app.chunking.chunker import chunk_document
from backend.app.embedding.embedder import Embedder
from backend.app.vector_store.qdrant_client import QdrantVectorStore


def generate_chunk_id(
    repository: str,
    file_path: str,
    chunk,
) -> str:

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

    return str(
        uuid.UUID(hash_value[:32])
    )
  

def reindex_file(
    repo_path: Path,
    file_path: str,
    repository: str,
):
    full_path = repo_path / file_path

    vector_store = QdrantVectorStore()
    embedder = Embedder()

    print(f"Reindexing file: {file_path}")

    # 1. Delete old chunks
    vector_store.delete_file_chunks(
    repository=repository,
    file_path=file_path,
)
    # 2. Check whether the file should be indexed
    if not full_path.exists():
        print("File no longer exists. Old chunks removed.")
        return

    if is_secret_file(full_path):
        print("Skipping secret file.")
        return

    if not is_supported_file(full_path):
        print("Skipping unsupported file.")
        return

    # 3. Read the updated file
    content = read_file(full_path)

    if not content.strip():
        print("File is empty.")
        return

    # 4. Create Document
    document = Document(
        repository=repository,
        file_path=Path(file_path),
        content=content,
        language=detect_language(full_path),
    )

    # 5. Create code-aware chunks
    chunks = chunk_document(document)

    print(f"Created {len(chunks)} chunks.")

    # 6. Generate embeddings and insert
    for chunk in chunks:

        vector = embedder.encode(chunk.content)

        point_id = generate_chunk_id(
            repository=repository,
            file_path=file_path,
            chunk=chunk,
        )

        vector_store.insert_chunk(
            point_id=point_id,
            vector=vector,
            chunk=chunk,
        )

    print("File reindexed successfully.")

def reindex_changed_files(
    repo_path: Path,
    repository: str,
    old_commit_hash: str,
    new_commit_hash: str,
):
    from backend.app.ingestion.git_history import (
        get_changed_files_between_commits,
    )

    changed_files = get_changed_files_between_commits(
        repo_path=repo_path,
        old_commit_hash=old_commit_hash,
        new_commit_hash=new_commit_hash,
    )

    print(
        f"Changed files between commits: {len(changed_files)}"
    )

    for file_path in changed_files:
        print(f"Reindexing changed file: {file_path}")

        reindex_file(
            repo_path=repo_path,
            file_path=file_path,
            repository=repository,
        )

    return changed_files

def update_index_if_stale(
    repo_path: Path,
    repository: str,
):
    from backend.app.ingestion.git_history import get_latest_commit
    from backend.app.ingestion.index_state import (
        get_indexed_commit_hash,
        save_index_state,
    )

    latest_commit = get_latest_commit(repo_path)
    indexed_commit = get_indexed_commit_hash(repository)

    if indexed_commit is None:
        print("No previous index state found.")
        return

    if indexed_commit == latest_commit["commit_hash"]:
        print("Index is already up to date.")
        return

    print("Index is stale.")
    print(f"Old commit: {indexed_commit}")
    print(f"New commit: {latest_commit['commit_hash']}")

    changed_files = reindex_changed_files(
        repo_path=repo_path,
        repository=repository,
        old_commit_hash=indexed_commit,
        new_commit_hash=latest_commit["commit_hash"],
    )

    save_index_state(
        repository=repository,
        commit_hash=latest_commit["commit_hash"],
    )

    print(
        f"Incremental reindex complete. "
        f"{len(changed_files)} files updated."
    )