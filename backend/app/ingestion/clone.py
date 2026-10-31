from pathlib import Path
from git import Repo

REPOSITORIES_DIR = Path("data/repositories")


def clone_repository(repo_url: str) -> Path:
    repo_name = repo_url.rstrip("/").split("/")[-1]

    if repo_name.endswith(".git"):
        repo_name = repo_name[:-4]

    repo_path = REPOSITORIES_DIR / repo_name

    REPOSITORIES_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    if repo_path.exists():
        print(f"Repository already exists: {repo_path}")
        return repo_path

    print(f"Cloning repository: {repo_url}")

    Repo.clone_from(
        repo_url,
        repo_path,
    )

    print(f"Repository cloned to: {repo_path}")

    return repo_path