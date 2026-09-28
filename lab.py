import argparse
import datetime
import sys

from src.load import load_corpus, load_questions

ALLOWED_STATUS = ("draft", "published", "superseded", "active")
ALLOWED_TYPE = ("policy", "help")
REQUIRED_DOC_FIELDS = ("id", "title", "type", "status", "updated")
REQUIRED_QUESTION_FIELDS = ("id", "question", "expected")


def main() -> None:
    parser = argparse.ArgumentParser(description="TechNova RAG Lab")
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("check", help="Check Python, the corpus, and the questions")
    sub.add_parser(
        "corpus",
        help="Print corpus id, type, status, and effective_date",
    )
    args = parser.parse_args()
    if args.command == "check":
        raise SystemExit(run_check())
    if args.command == "corpus":
        raise SystemExit(run_corpus())
    parser.print_help()


def run_check() -> int:
    print("TechNova RAG Lab")
    version = (
        f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    )
    if (sys.version_info.major, sys.version_info.minor) != (3, 12):
        print(f"[FAIL] Python 3.12 required, found {version}")
        return 1
    print(f"[OK] Python {version}")

    doc_problems = []
    docs = None
    try:
        docs = load_corpus()
    except Exception as exc:
        doc_problems.append(f"could not read corpus: {exc}")

    if docs is not None:
        seen = set()
        for doc in docs:
            meta = doc.meta if isinstance(doc.meta, dict) else {}
            name = doc.path.replace("\\", "/").rsplit("/", 1)[-1]
            for field in REQUIRED_DOC_FIELDS:
                if field not in meta or meta[field] is None or str(meta[field]) == "":
                    doc_problems.append(f"{name} missing {field}")
            file_id = name[:-3] if name.endswith(".md") else name
            if doc.id != file_id:
                doc_problems.append(f"{name} id {doc.id} does not match file name")
            if doc.id in seen:
                doc_problems.append(f"duplicate id {doc.id}")
            else:
                seen.add(doc.id)
            status = meta.get("status")
            if status not in (None, "") and status not in ALLOWED_STATUS:
                doc_problems.append(f"{name} status {status} is not allowed")
            kind = meta.get("type")
            if kind not in (None, "") and kind not in ALLOWED_TYPE:
                doc_problems.append(f"{name} type {kind} is not allowed")
        if not doc_problems:
            print(f"[OK] Corpus loaded: {len(docs)} documents")

    question_problems = []
    questions = None
    try:
        questions = load_questions()
    except Exception as exc:
        question_problems.append(f"could not read questions: {exc}")

    if questions is not None:
        known = {doc.id for doc in docs} if docs is not None else None
        for index, item in enumerate(questions, start=1):
            if not isinstance(item, dict):
                question_problems.append(f"question {index} is not a record")
                continue
            qid = item.get("id") or f"question {index}"
            for field in REQUIRED_QUESTION_FIELDS:
                if field not in item or item[field] is None or str(item[field]) == "":
                    question_problems.append(f"{qid} missing {field}")
            expected = item.get("expected")
            if (
                known is not None
                and expected not in (None, "")
                and expected not in known
            ):
                question_problems.append(
                    f"{qid} expected {expected} is not in the corpus"
                )
        if not question_problems:
            print(f"[OK] Evaluation questions: {len(questions)}")

    problems = doc_problems + question_problems
    if problems:
        for problem in problems:
            print(f"[FAIL] {problem}")
        return 1

    print("Ready.")
    return 0


def run_corpus() -> int:
    docs = load_corpus()
    header = ("id", "type", "status", "effective_date")
    rows = [header]
    for doc in docs:
        meta = doc.meta if isinstance(doc.meta, dict) else {}
        rows.append(
            (
                doc.id,
                "" if meta.get("type") is None else str(meta.get("type")),
                "" if meta.get("status") is None else str(meta.get("status")),
                _effective_date(meta.get("effective_date")),
            )
        )
    widths = [0, 0, 0, 0]
    for row in rows:
        for index, cell in enumerate(row):
            widths[index] = max(widths[index], len(cell))
    for row in rows:
        pieces = [cell.ljust(widths[index]) for index, cell in enumerate(row)]
        print("  ".join(pieces).rstrip())
    return 0


def _effective_date(value) -> str:
    if value is None or value == "":
        return "-"
    if isinstance(value, datetime.datetime):
        return value.date().isoformat()
    if isinstance(value, datetime.date):
        return value.isoformat()
    return str(value)


if __name__ == "__main__":
    main()
