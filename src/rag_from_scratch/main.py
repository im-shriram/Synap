import os
from typing import Any
import pathlib
from dotenv import load_dotenv

from tasks import DocumentLoader, TextSplitter, Embedding
from components import Retrievar, CustomPromptTemplate, Models, Parsers, ChatHistory

from langchain_groq import ChatGroq
from langchain_core.output_parsers.json import JsonOutputParser
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_core.prompt_values import PromptValue
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough, RunnableAssign, RunnableSerializable

class Runnable:
    def __init__(self) -> None:
        self.models_obj = Models()
        self.retrievar_obj = Retrievar()
        self.template_obj = CustomPromptTemplate()
        self.memory_obj = ChatHistory()

        self.document_loder_obj = DocumentLoader()
        self.text_splitter_obj = TextSplitter()
        self.embedding_obj = Embedding(model=self.models_obj.embedding_model)

        self.previous_chat_history = self.memory_obj.load_chat_history(path=pathlib.Path(__file__).parent.parent.parent / "data" / "artifacts" / "chat_history.json")
        self.system_prompt: PromptValue = self.template_obj.system_prompt_template.invoke(input={"previous_chat_history": self.previous_chat_history})
        self.current_chat_history: list[BaseMessage] = self.system_prompt.to_messages()
    
    def embedding_chain(self: Runnable) -> RunnableSerializable:
        document_loading: RunnableLambda = RunnableLambda(func=self.document_loder_obj.load_documents)
        text_splitting: RunnableLambda = RunnableLambda(func=self.text_splitter_obj.split_documents)
        docs_embedding: RunnableLambda = RunnableLambda(func=self.embedding_obj.embed_docs)
        storing: RunnableLambda = RunnableLambda(func=self.embedding_obj.store_embeddings)

        return document_loading | text_splitting | docs_embedding | storing

    def response_chain(self) -> RunnableSerializable:
        query_embedding: RunnableLambda = RunnableLambda(func=self.embedding_obj.embed_query)
        query_embedding_with_input: RunnableAssign = RunnablePassthrough.assign(
            query_embedding=query_embedding
        )
        retrievar: RunnableLambda = RunnableLambda(func=self.retrievar_obj.retrieval)
        query_with_relevent_docs: RunnableAssign = RunnablePassthrough.assign(
            relevent_docs=query_embedding_with_input | retrievar,
        )
        prompt_template: PromptTemplate = CustomPromptTemplate().user_prompt_template

        def update_chat_history(args: Any):
            if type(args) == dict:
                self.current_chat_history.append(AIMessage(content=args["summary"]))
                # print(f"First: {self.current_chat_history}")
                return args
            else:
                self.current_chat_history.append(HumanMessage(content=args.text))
                # print(f"Second: {self.current_chat_history} \n")
                return self.current_chat_history 

        chat_history_runnable: RunnableLambda = RunnableLambda(func=update_chat_history)

        model: ChatGroq = Models().chat_model
        parser: JsonOutputParser = Parsers().json_parser()

        return query_with_relevent_docs | prompt_template | chat_history_runnable | model | parser | chat_history_runnable

def main():
    load_dotenv(dotenv_path=pathlib.Path(__file__).parent.parent.parent / ".env")
    obj = Runnable()

    if False:
        obj.embedding_chain().invoke(input=pathlib.Path(__file__).parent.parent.parent / "data" / "docs")

    while True:
        query: str = input("You: ")
        if query.lower().strip() == "exit":
            break

        result = obj.response_chain().invoke(
            input={
                "query": query,
                "docs_embeddings": obj.embedding_obj.load_embeddings(),
                "knowledge_base": obj.text_splitter_obj.load_chunks()
            }
        ); print(f"Model: {result}")

    obj.memory_obj.save_chat_history(chat_history=obj.current_chat_history, path=pathlib.Path(__file__).parent.parent.parent / "data" / "artifacts" / "chat_history.json")

if __name__ == "__main__":
    main()