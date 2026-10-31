from backend.app.chunking.code_chunk import CodeChunk


def chunk_python(document):
    from tree_sitter import Language, Parser
    import tree_sitter_python

    parser = Parser()
    parser.language = Language(tree_sitter_python.language())

    tree = parser.parse(document.content.encode("utf-8"))

    chunks = []

    def walk(node, parent_class=None):
        if node.type == "class_definition":
            class_name = document.content[
                node.child_by_field_name("name").start_byte:
                node.child_by_field_name("name").end_byte
            ]

            for child in node.children:
                if child.type in ("function_definition", "async_function_definition"):
                    method_name = document.content[
                        child.child_by_field_name("name").start_byte:
                        child.child_by_field_name("name").end_byte
                    ]

                    chunks.append(
                        CodeChunk(
                            repository=document.repository,
                            file_path=document.file_path,
                            language=document.language,
                            chunk_type="method",
                            symbol_name=f"{class_name}.{method_name}",
                            start_line=child.start_point[0] + 1,
                            end_line=child.end_point[0] + 1,
                            content=document.content[
                                child.start_byte:child.end_byte
                            ],
                        )
                    )

                else:
                    walk(child, class_name)

        elif node.type in ("function_definition", "async_function_definition"):
            function_name = document.content[
                node.child_by_field_name("name").start_byte:
                node.child_by_field_name("name").end_byte
            ]

            chunks.append(
                CodeChunk(
                    repository=document.repository,
                    file_path=document.file_path,
                    language=document.language,
                    chunk_type="function",
                    symbol_name=function_name,
                    start_line=node.start_point[0] + 1,
                    end_line=node.end_point[0] + 1,
                    content=document.content[
                        node.start_byte:node.end_byte
                    ],
                )
            )

        else:
            for child in node.children:
                walk(child, parent_class)

    walk(tree.root_node)

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
            CodeChunk(
                repository=document.repository,
                file_path=document.file_path,
                language=document.language,
                chunk_type="document",
                symbol_name=f"document_{len(chunks) + 1}",
                start_line=start + 1,
                end_line=end,
                content=content,
            )
        )

    return chunks


def chunk_javascript(document):
    """
    Basic code-aware chunking for JavaScript/JSX/TypeScript.

    This intentionally starts with function/component blocks and
    falls back to line-based chunks when a block cannot be detected.
    """

    lines = document.content.splitlines()
    chunks = []

    current = []
    start_line = 1
    brace_count = 0
    symbol_name = None

    for index, line in enumerate(lines, start=1):

        stripped = line.strip()

        if not current:
            start_line = index

            if (
                stripped.startswith("function ")
                or stripped.startswith("async function ")
                or stripped.startswith("const ")
                or stripped.startswith("export function ")
                or stripped.startswith("export const ")
                or stripped.startswith("export default function ")
            ):
                symbol_name = stripped.split("(")[0].split("=")[0].strip()

        current.append(line)

        brace_count += line.count("{")
        brace_count -= line.count("}")

        if current and brace_count <= 0 and ("{" in "\n".join(current)):
            content = "\n".join(current)

            chunks.append(
                CodeChunk(
                    repository=document.repository,
                    file_path=document.file_path,
                    language=document.language,
                    chunk_type="function",
                    symbol_name=symbol_name or f"code_block_{len(chunks) + 1}",
                    start_line=start_line,
                    end_line=index,
                    content=content,
                )
            )

            current = []
            brace_count = 0
            symbol_name = None

    if current:
        chunks.append(
            CodeChunk(
                repository=document.repository,
                file_path=document.file_path,
                language=document.language,
                chunk_type="code",
                symbol_name=f"code_block_{len(chunks) + 1}",
                start_line=start_line,
                end_line=len(lines),
                content="\n".join(current),
            )
        )

    return chunks


def chunk_document(document):

    language = (document.language or "").lower()
    file_path = str(document.file_path).lower()

    if language == "python":
        return chunk_python(document)

    if language in {
        "javascript",
        "javascriptreact",
        "jsx",
        "typescript",
        "typescriptreact",
    }:
        return chunk_javascript(document)

    if (
        language in {"markdown", "text", "plaintext"}
        or file_path.endswith(".md")
        or file_path.endswith(".txt")
        or file_path.endswith("readme")
    ):
        return chunk_text(document)

    return []