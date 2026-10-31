from pathlib import Path

from reader import read_file
from language import detect_language
from document import Document


def load_documents(
    repository_path: Path,
    file_paths: list[Path],
) -> list[Document]:
    documents = []

    repository_name = repository_path.name

    for file_path in file_paths:
        content = read_file(file_path)

        if not content:
            continue

        relative_path = file_path.relative_to(repository_path)

        document = Document(
            repository=repository_name,
            file_path=relative_path,
            content=content,
            language=detect_language(file_path),
        )

        documents.append(document)

    return documents