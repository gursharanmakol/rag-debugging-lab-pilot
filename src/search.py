from dataclasses import dataclass

import numpy as np

from src.eligibility import is_eligible
from src.embed import embed_documents, embed_query, load_model


@dataclass
class Index:
    docs: list
    matrix: np.ndarray
    model: object

    def rank(self, query: str) -> list:
        vector = embed_query(self.model, query)
        scores = self.matrix @ vector
        order = sorted(
            range(len(self.docs)),
            key=lambda index: (-float(scores[index]), self.docs[index].id),
        )
        return [
            (self.docs[index], float(scores[index]))
            for index in order
        ]

    def search(self, query: str, k: int = 3) -> list:
        return self.rank(query)[:k]


def build_index(docs, model=None) -> Index:
    if model is None:
        model = load_model()
    matrix = embed_documents(model, docs)
    return Index(docs=list(docs), matrix=matrix, model=model)


def searchable_documents(docs):
    return [doc for doc in docs if is_eligible(doc)]


def eligible_results(index, query, k=3):
    allowed = {doc.id for doc in searchable_documents(index.docs)}
    ranked = [
        (doc, score)
        for doc, score in index.rank(query)
        if doc.id in allowed
    ]
    return ranked[:k]
