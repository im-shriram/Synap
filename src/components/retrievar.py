from typing import Any
class Retrievar:
    def __init__(self: Retrievar) -> None:
        self.similarity_scores: list[float] = []
        self.data_with_scores: list[tuple[str, float]] = []
        self.relevent_docs: list[str] = []

    def semantic_search(self: Retrievar, query_embedding: list[float], docs_embeddings: list[list[float]]):
        similarity_scores: list[float] = []

        for doc_embeddings in docs_embeddings:
            similarity = 0
            for i, j in zip(query_embedding, doc_embeddings):
                similarity += (i * j)
            similarity_scores.append(similarity)
        
        return similarity_scores

    def retrieval(
        self: Retrievar, 
        kwargs: dict
    ):
        self.similarity_scores = self.semantic_search(query_embedding=kwargs["query_embedding"], docs_embeddings=kwargs["docs_embeddings"])
        self.data_with_scores = list(zip(kwargs["knowledge_base"], self.similarity_scores))

        self.data_with_scores.sort(reverse=True, key=lambda a: a[1])
        for doc, _ in self.data_with_scores[:5]:
            self.relevent_docs.append(doc)
        
        return self.relevent_docs
        