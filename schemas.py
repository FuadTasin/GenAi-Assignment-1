from dataclasses import field
from pydantic import BaseModel,Field
from langchain_core.output_parsers import StrOutputParser,PydanticOutputParser

class Response(BaseModel):
    answer:str=Field(description="The answer to the user's response.Make it relavent to the question.")
    summary:str=Field(description="Give the summary of the the answer.")
    confidence:float=Field(gt=0,lt=1,description="The confidence should be between 0 to 1.")
    category:str=Field(description="The category of the user's question.The categories are Mathematical,Programming & General")
    keywords:list[str]=Field(description="Give the keyword from the response")

pydantic_output_parser=PydanticOutputParser(pydantic_object=Response)
str_output_parser=StrOutputParser()