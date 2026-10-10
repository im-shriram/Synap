import pathlib
import json

class TextSplitter:
    def __init__(self: TextSplitter, chunk_size: int = 500) -> None:
        self.chunk_size: int = chunk_size
        self.knowledge_base: list[str] = []
        self.save_path: pathlib.Path = pathlib.Path(__file__).parent.parent.parent / "data" / "artifacts" 
    
    def split_documents(self: TextSplitter, doc: str) -> list[str]:
        self.knowledge_base = []
        string: str = ""

        for idx, char in enumerate(doc):
            string += char

            if (idx + 1) >= len(doc) or (idx + 1) % self.chunk_size == 0:
                if string.strip() != "":
                    self.knowledge_base.append(string.strip())
                string = ""
        
        self.save_chunks(chunks=self.knowledge_base)        
        return self.knowledge_base

    def save_chunks(self: TextSplitter, chunks: list[str]) -> None:
        with open(file=self.save_path / "chunks.json", mode='w') as fp:
            json.dump(obj=chunks, fp=fp)

    def load_chunks(self: TextSplitter) -> str:
        with open(file=self.save_path / "chunks.json", mode='r') as fp:
            chunks: list[str] = json.load(fp=fp)
            return chunks