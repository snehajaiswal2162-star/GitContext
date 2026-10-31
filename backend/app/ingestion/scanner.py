from pathlib import Path


def scan_repository(repo_path: Path) -> list[Path]:
    files = []

    for path in repo_path.rglob("*"):
        if path.is_file():
            files.append(path)

    return files