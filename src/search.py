from dataclasses import dataclass

import numpy as np

from src.embed import embed_documents, embed_query, load_model


@dataclass
class Index:
    docs: list
    matrix: np.ndarray
    model: object

    def search(self, query: str, k: int = 3) -> list:
        vector = embed_query(self.model, query)
        scores = self.matrix @ vector
        order = sorted(
            range(len(self.docs)),
            key=lambda index: (-float(scores[index]), self.docs[index].id),
        )
        return [
            (self.docs[index], float(scores[index]))
            for index in order[:k]
        ]


def build_index(docs, model=None) -> Index:
    if model is None:
        model = load_model()
    matrix = embed_documents(model, docs)
    return Index(docs=list(docs), matrix=matrix, model=model)
