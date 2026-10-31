from pathlib import Path
import json


INDEX_STATE_FILE = Path("data/index_state.json")


def _load_states() -> dict:
    if not INDEX_STATE_FILE.exists():
        return {}

    data = json.loads(
        INDEX_STATE_FILE.read_text(
            encoding="utf-8"
        )
    )

    # Convert old single-repository format
    # into the new multi-repository format.
    if "repository" in data:
        return {
            data["repository"]: {
                "commit_hash": data["commit_hash"]
            }
        }

    return data


def save_index_state(
    repository: str,
    commit_hash: str,
):
    INDEX_STATE_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    states = _load_states()

    states[repository] = {
        "commit_hash": commit_hash
    }

    INDEX_STATE_FILE.write_text(
        json.dumps(
            states,
            indent=4
        ),
        encoding="utf-8",
    )


def load_index_state(
    repository: str | None = None,
) -> dict | None:

    states = _load_states()

    if repository is None:
        if not states:
            return None

        repository = next(iter(states))

    state = states.get(repository)

    if state is None:
        return None

    return {
        "repository": repository,
        "commit_hash": state["commit_hash"],
    }


def is_index_stale(
    repo_path: Path,
) -> bool:

    from backend.app.ingestion.git_history import (
        get_latest_commit
    )

    latest_commit = get_latest_commit(repo_path)

    repository = repo_path.name

    indexed_state = load_index_state(
        repository
    )

    if indexed_state is None:
        return True

    return (
        latest_commit["commit_hash"]
        != indexed_state["commit_hash"]
    )


def get_indexed_commit_hash(
    repository: str | None = None,
) -> str | None:

    state = load_index_state(
        repository
    )

    if state is None:
        return None

    return state["commit_hash"]