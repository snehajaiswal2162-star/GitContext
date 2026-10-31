def build_context(results: list) -> str:
    context_parts = []

    for result in results:
        chunk = result["chunk"]

        context_parts.append(
            f"Repository: {chunk.repository}\n"
            f"File: {chunk.file_path}\n"
            f"Language: {chunk.language}\n"
            f"Type: {chunk.chunk_type}\n"
            f"Symbol: {chunk.symbol_name}\n"
            f"Lines: {chunk.start_line}-{chunk.end_line}\n\n"
            f"{chunk.content}\n"
        )

    return "\n" + ("\n" + "=" * 60 + "\n").join(context_parts)