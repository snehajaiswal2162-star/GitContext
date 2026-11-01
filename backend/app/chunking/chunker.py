
from backend.app.chunking.code_chunk import CodeChunk


def _make_chunk(document, chunk_type, symbol_name, start_line, end_line, content):
    return CodeChunk(
        repository=document.repository,
        file_path=str(document.file_path),
        language=document.language,
        chunk_type=chunk_type,
        symbol_name=symbol_name,
        start_line=start_line,
        end_line=end_line,
        content=content,
    )


def chunk_python(document):
    from tree_sitter import Language, Parser
    import tree_sitter_python

    source = document.content
    source_bytes = source.encode("utf-8")

    parser = Parser()
    parser.language = Language(tree_sitter_python.language())
    tree = parser.parse(source_bytes)

    chunks = []
    module_nodes = []

    def node_text(node):
        return source_bytes[node.start_byte:node.end_byte].decode("utf-8")

    def get_name(node):
        name_node = node.child_by_field_name("name")
        return node_text(name_node) if name_node else "anonymous"

    for node in tree.root_node.children:
        if node.type in ("function_definition", "async_function_definition"):
            chunks.append(
                _make_chunk(
                    document,
                    "function",
                    get_name(node),
                    node.start_point[0] + 1,
                    node.end_point[0] + 1,
                    node_text(node),
                )
            )

        elif node.type == "class_definition":
            class_name = get_name(node)

            # Keep the complete class as architectural context.
            chunks.append(
                _make_chunk(
                    document,
                    "class",
                    class_name,
                    node.start_point[0] + 1,
                    node.end_point[0] + 1,
                    node_text(node),
                )
            )

            # Also create individual method chunks for precise retrieval.
            for child in node.children:
                if child.type in (
                    "function_definition",
                    "async_function_definition",
                ):
                    chunks.append(
                        _make_chunk(
                            document,
                            "method",
                            f"{class_name}.{get_name(child)}",
                            child.start_point[0] + 1,
                            child.end_point[0] + 1,
                            node_text(child),
                        )
                    )
        else:
            module_nodes.append(node)

    # Capture imports, constants, and other module-level setup.
    if module_nodes:
        module_content = "\n".join(
            node_text(node)
            for node in module_nodes
            if node.type not in ("comment",)
        ).strip()

        if module_content:
            first_node = module_nodes[0]
            last_node = module_nodes[-1]

            chunks.append(
                _make_chunk(
                    document,
                    "module",
                    "module_setup",
                    first_node.start_point[0] + 1,
                    last_node.end_point[0] + 1,
                    module_content,
                )
            )

    # Fallback for files with no recognized definitions.
    if not chunks and source.strip():
        return chunk_text(document)

    return chunks


def chunk_text(document, lines_per_chunk=40):
    lines = document.content.splitlines()
    chunks = []

    for start in range(0, len(lines), lines_per_chunk):
        end = min(start + lines_per_chunk, len(lines))
        content = "\n".join(lines[start:end])

        if not content.strip():
            continue

        chunks.append(
            _make_chunk(
                document,
                "document",
                f"document_{len(chunks) + 1}",
                start + 1,
                end,
                content,
            )
        )

    return chunks


def chunk_javascript(document):
    # Line-based fallback avoids unreliable brace counting.
    return chunk_text(document, lines_per_chunk=50)


def chunk_document(document):
    language = (document.language or "").lower()
    file_path = str(document.file_path).lower()

    if language == "python" or file_path.endswith(".py"):
        return chunk_python(document)

    if language in {
        "javascript",
        "javascriptreact",
        "jsx",
        "typescript",
        "typescriptreact",
    } or file_path.endswith((".js", ".jsx", ".ts", ".tsx")):
        return chunk_javascript(document)

    # Keep other supported source files searchable too.
    return chunk_text(document)
