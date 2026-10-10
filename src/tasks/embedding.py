import json
import pathlib

from langchain_google_genai import GoogleGenerativeAIEmbeddings

class Embedding:
    def __init__(self: Embedding, model: GoogleGenerativeAIEmbeddings) -> None:
        self.embedding_model: GoogleGenerativeAIEmbeddings = model
        self.query_embeddings: list[float] | None = None
        self.docs_embeddings: list[list[float]] | None = None
        self.store_path = pathlib.Path(__file__).parent.parent.parent / "data" / "embeddings" / "knowledge_base.json"

    def embed_query(self: Embedding, query: dict) -> list[float]:
        self.query_embeddings: list[float] = self.embedding_model.embed_query(text=query['query'])
        return self.query_embeddings

    def embed_docs(self: Embedding, docs: list[str]) -> list[list[float]]:
        self.docs_embeddings: list[list[float]] = self.embedding_model.embed_documents(texts=docs)
        return self.docs_embeddings
    
    def load_embeddings(self: Embedding) -> list[list[float]]:
        with open(file=self.store_path, mode='r') as fp:
            embeddings = json.load(fp=fp)
        return embeddings

    def store_embeddings(self, embeddings: list[list[float]]) -> list[list[float]]:
        """ We are only storing embeddings of knowledge base in json format """
        self.store_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file=self.store_path, mode='w') as fp:
            json.dump(obj=embeddings, fp=fp)
        return embeddings