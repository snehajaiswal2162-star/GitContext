from dataclasses import dataclass
from pathlib import Path


@dataclass
class Document:
    repository: str
    file_path: Path
    content: str
    language: str