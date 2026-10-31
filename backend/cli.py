import argparse
import requests


def main():
    parser = argparse.ArgumentParser(
        description="GitContext - Codebase Intelligence CLI"
    )

    parser.add_argument(
        "--version",
        action="version",
        version="GitContext 1.0.0",
    )

    subparsers = parser.add_subparsers(dest="command")

    # ---------------- INDEX ----------------

    index_parser = subparsers.add_parser(
        "index",
        help="Index a GitHub repository",
    )

    index_parser.add_argument(
        "repository_url",
        help="GitHub repository URL",
    )

    # ---------------- ASK ----------------

    ask_parser = subparsers.add_parser(
        "ask",
        help="Ask a question about a repository",
    )

    ask_parser.add_argument(
        "question",
        help="Question to ask",
    )

    ask_parser.add_argument(
        "repository_url",
        help="GitHub repository URL",
    )

    args = parser.parse_args()

    # ---------------- INDEX ----------------

    if args.command == "index":

        print(
            f"Indexing repository: {args.repository_url}"
        )

        response = requests.post(
            "http://127.0.0.1:8000/repositories/index",
            json={
                "repository_url": args.repository_url
            },
        )

        if response.ok:

            data = response.json()

            print(data["message"])

        else:

            print(
                f"Indexing failed: {response.status_code}"
            )

            print(response.text)

    # ---------------- ASK ----------------

    elif args.command == "ask":

        print(
            f"Question: {args.question}"
        )

        response = requests.post(
            "http://127.0.0.1:8000/ask",
            json={
                "question": args.question,
                "repository_url": args.repository_url,
            },
        )

        if response.ok:

            data = response.json()

            print("\nAnswer:")
            print(data["answer"])

            if data.get("citations"):

                print("\nCitations:")

                for citation in data["citations"]:

                    print(
                        f"- {citation['file_path']} "
                        f"({citation['symbol_name']}, "
                        f"lines {citation['start_line']}-"
                        f"{citation['end_line']})"
                    )

        else:

            print(
                f"Question failed: {response.status_code}"
            )

            print(response.text)


if __name__ == "__main__":
    main()