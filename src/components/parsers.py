from typing import Optional
from pydantic import BaseModel, Field

from langchain_core.output_parsers import JsonOutputParser, StrOutputParser

from pydantic import BaseModel, Field

class Schema(BaseModel):
    main_explanation: str = Field(
        description=(
            "A comprehensive, beautifully formatted Markdown string. It must combine "
            "the problem definition, a relatable analogy, an in-depth explanation "
            "(using the Why-What-How framework - Optional), structured Markdown tables for organizing data, "
            "any required math derivations (formatted in valid LaTeX like $...$ or $$...$$), "
            "and clean code snippets if required in markdown code blocks."
            "Adjust the response based on user query and system instructions."
            "For Out-of-Scope / General Queries, add the relevent responses in this block"
        ),
    )

    summary: str = Field(
        description=(
            "A concise, pure text summary (5 lines) of the overall response. "
            "It must contain no Markdown formatting, capturing the central issue and core takeaway plainly."
            "For Out-of-Scope / General Queries, simply returns this field with empty string"
        )
    )

class Parsers:
    def json_parser(self) -> JsonOutputParser:
        return JsonOutputParser(pydantic_object=Schema)

    def string_parser(self) -> StrOutputParser:
        return StrOutputParser()