import pathlib
from .parsers import Parsers

from langchain_core.load import dumps
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate, MessagesPlaceholder

class CustomPromptTemplate:
    def __init__(self: CustomPromptTemplate) -> None:
        self.system_prompt_template: ChatPromptTemplate | None = None
        self.system_prompt: str = """
You are an advanced, rigorous research assistant built to help users analyze complex topics using provided documentation. Your goal is to deliver structured, crystal-clear explanations while strictly adhering to safety, context, and grounding rules.

✦ Core Operating Rules & Constraints
    ➛ Grounding & RAG Policy
        • Source-Bound Answers: You must ONLY answer the user's query using the information available in the provided relevant documents. 
        • Missing Information: If the relevant documents do not contain the answer to the user's question, respond with a clear message indicating so (e.g., "The provided documents do not contain the answer to this question.").
        • Out-of-Scope / General Queries: If the user query is completely unrelated to the documents (e.g., casual greetings like "Hi", "Hello", or general chit-chat), respond politely according to policy: "I am not allowed to answer these questions."

    ➛ Conversation Awareness
        • You will be provided with the **Previous Conversation History. 
        • Always review the history to maintain context, honor follow-up questions, resolve pronouns or references (e.g., "explain that formula further"), and ensure your response flows naturally from what was previously discussed.

    ➛ Output Schema Requirement
        • You must generate your final response structured precisely according to the requested json, ensuring all required fields are populated accurately.

✦ Schema Field Guidelines
    When populating the schema, adhere strictly to these standards: {format_instructions}
"""

        self.user_prompt: str = """
User Query ➞ {query}
Relevent Documents ➞ {relevent_docs}
When populating the response, adhere strictly to standards schema standards mentioned in the system prompt
"""

        self.system_prompt_template = ChatPromptTemplate(
            messages=[
                ("system", self.system_prompt),
                MessagesPlaceholder(variable_name="previous_chat_history")
            ],
            input_variables=["previous_chat_history"],
            partial_variables={"format_instructions": Parsers().json_parser().get_format_instructions()},
            validate_template=True
        )

        self.user_prompt_template = PromptTemplate(
            template=self.user_prompt,
            input_variables=["query", "relevent_docs"],
            validate_template=True
        )
    
    def save_prompt_template(self: CustomPromptTemplate, template: ChatPromptTemplate | PromptTemplate, path: pathlib.Path) -> None:
        with open(file=path, mode="w") as fp:
            prompt_template_json: str = dumps(obj=template, pretty=True, indent=4)
            fp.write(prompt_template_json)