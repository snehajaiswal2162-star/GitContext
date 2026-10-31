from dataclasses import dataclass


@dataclass
class CodeChunk:
    repository: str
    file_path: str
    language: str
    chunk_type: str
    symbol_name: str
    start_line: int
    end_line: int
    content: str