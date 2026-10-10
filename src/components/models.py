import os
from langchain_cohere import CohereEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_groq import ChatGroq

class Models:
    def __init__(self):
        # self.embedding_model = GoogleGenerativeAIEmbeddings(
        #     model="gemini-embedding-2-preview",
        #     output_dimensionality=768,
        #     task_type="RETRIEVAL_QUERY",
        #     google_api_key=os.getenv("GOOGLE_API_KEY")
        # )

        self.embedding_model = CohereEmbeddings(
            model="embed-english-light-v3.0",
            cohere_api_key=os.getenv(key="COHERE_API_KEY"),
            embedding_types=['float']
        )

        self.chat_model: ChatGroq = ChatGroq(
            model="openai/gpt-oss-120b",
            temperature=0.2,

            max_tokens=4096,
            reasoning_effort="low",
            reasoning_format="parsed",

            groq_api_key=os.getenv("GROQ_API_TOKEN"),
            timeout=None, # The timeout for API requests in seconds. None uses the default
            max_retries=2, # Maximum number of retries for a failed request. Default is 2
        )

        # self.chat_model: ChatGoogleGenerativeAI = ChatGoogleGenerativeAI(
        #     model="gemini-3-flash-preview",
        #     api_key=os.getenv("GOOGLE_API_KEY"),
        #     temperature=0.2,
        #     max_tokens=2048,
        #     reasoning_effort="low",
        #     include_thoughts=True
        # )