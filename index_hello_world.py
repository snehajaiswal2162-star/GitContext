
from pathlib import Path

from backend.app.ingestion.reindex import reindex_file

reindex_file(
    repo_path=Path("data/repositories/Hello-World"),
    file_path="README",
    repository="Hello-World",
)
