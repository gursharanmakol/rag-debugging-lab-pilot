import os
from pathlib import Path

import numpy as np
from model2vec import StaticModel

MODEL_DIR = Path(__file__).resolve().parent.parent / "models" / "potion-base-8M"


def load_model(model_dir=MODEL_DIR):
    os.environ["HF_HUB_OFFLINE"] = "1"
    return StaticModel.from_pretrained(Path(model_dir))


def document_text(doc) -> str:
    return doc.meta["title"] + "\n\n" + doc.text


def embed_texts(model, texts) -> np.ndarray:
    encoded = model.encode(list(texts))
    matrix = np.asarray(encoded, dtype=np.float32)
    if matrix.ndim == 1:
        matrix = matrix.reshape(1, -1)
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    norms = np.maximum(norms, np.float32(1e-12))
    return (matrix / norms).astype(np.float32)


def embed_documents(model, docs) -> np.ndarray:
    return embed_texts(model, [document_text(doc) for doc in docs])


def embed_query(model, question) -> np.ndarray:
    return embed_texts(model, [question])[0]
