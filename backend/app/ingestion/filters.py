from pathlib import Path


IGNORED_DIRECTORIES = {
    ".git",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    "env",
    "dist",
    "build",
}


SUPPORTED_EXTENSIONS = {
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".java",
    ".c",
    ".cpp",
    ".h",
    ".hpp",
    ".go",
    ".rs",
    ".php",
    ".rb",
    ".swift",
    ".kt",
    ".kts",
    ".html",
    ".css",
    ".scss",
    ".sql",
    ".json",
    ".yaml",
    ".yml",
    ".md",
    ".txt",
}


SUPPORTED_FILENAMES = {
    "README",
    "LICENSE",
    "CHANGELOG",
}


SECRET_FILENAMES = {
    ".env",
    ".env.local",
    ".env.production",
    ".env.development",
    "credentials.json",
    "secrets.json",
    "secret.json",
}


SECRET_EXTENSIONS = {
    ".pem",
    ".key",
    ".p12",
    ".pfx",
}


def should_ignore(path: Path) -> bool:
    return any(part in IGNORED_DIRECTORIES for part in path.parts)


def is_supported_file(path: Path) -> bool:
    if path.name.upper() in SUPPORTED_FILENAMES:
        return True

    return path.suffix.lower() in SUPPORTED_EXTENSIONS


def is_secret_file(path: Path) -> bool:
    if path.name in SECRET_FILENAMES:
        return True

    return path.suffix.lower() in SECRET_EXTENSIONS


def filter_files(files: list[Path]) -> list[Path]:
    return [
        path
        for path in files
        if not should_ignore(path)
        and not is_secret_file(path)
        and is_supported_file(path)
    ]