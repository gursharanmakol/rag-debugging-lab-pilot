from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass
class Document:
    id: str
    meta: dict
    text: str
    path: str


def load_corpus(folder: str = "corpus") -> list[Document]:
    root = Path(folder)
    documents = []
    for path in root.glob("*.md"):
        if path.name == "METADATA.md":
            continue
        raw = path.read_text(encoding="utf-8")
        meta, body = _split_front_matter(raw, path.name)
        documents.append(
            Document(
                id=meta["id"],
                meta=meta,
                text=body,
                path=str(path),
            )
        )
    documents.sort(key=lambda document: document.id)
    return documents


def _split_front_matter(raw: str, name: str) -> tuple[dict, str]:
    normalized = raw.replace("\r\n", "\n").replace("\r", "\n")
    marker = "---\n"
    start = normalized.find(marker)
    if start == -1:
        raise ValueError(f"{name} has no front matter")
    end = normalized.find(marker, start + len(marker))
    if end == -1:
        raise ValueError(f"{name} has no closing front matter marker")
    front = normalized[start + len(marker) : end]
    body = normalized[end + len(marker) :]
    meta = yaml.safe_load(front)
    if not isinstance(meta, dict):
        raise ValueError(f"{name} front matter is not a mapping")
    return meta, body


def load_questions(path: str = "eval/questions.yaml") -> list[dict]:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    if isinstance(data, dict) and isinstance(data.get("questions"), list):
        return data["questions"]
    raise ValueError("questions file must contain a questions list")
