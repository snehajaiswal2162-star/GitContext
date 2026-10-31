from pathlib import Path
from git import Repo


def get_latest_commit(repo_path: Path) -> dict:

    repo = Repo(repo_path)

    commit = repo.head.commit

    return {
        "commit_hash": commit.hexsha,
        "short_hash": commit.hexsha[:7],
        "message": commit.message.strip(),
        "author": str(commit.author),
        "committed_at": commit.committed_datetime,
    }


def get_changed_files(
    repo_path: Path,
    commit_hash: str,
) -> list[str]:

    repo = Repo(repo_path)

    commit = repo.commit(commit_hash)

    changed_files = []

    if commit.parents:
        parent = commit.parents[0]

        for item in parent.diff(commit):
            changed_files.append(item.b_path or item.a_path)

    return changed_files

def get_changed_files_between_commits(
    repo_path: Path,
    old_commit_hash: str,
    new_commit_hash: str,
) -> list[str]:

    repo = Repo(repo_path)

    old_commit = repo.commit(old_commit_hash)
    new_commit = repo.commit(new_commit_hash)

    changed_files = set()

    for item in old_commit.diff(new_commit):
        file_path = item.b_path or item.a_path

        if file_path:
            changed_files.add(file_path)

    return sorted(changed_files)