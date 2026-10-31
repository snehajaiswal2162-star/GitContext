def create_citation(chunk) -> dict:
    return {
        "repository": chunk.repository,
        "file_path": str(chunk.file_path),
        "symbol_name": chunk.symbol_name,
        "start_line": chunk.start_line,
        "end_line": chunk.end_line,
    }