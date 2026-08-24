from dataclasses import field
from pydantic import BaseModel,Field

class Response(BaseModel):
    answer:str=Field(description="")
    summary:str=Field(description="Give the summary of the question within 1-3 sentences.")
    confidence:float=Field(gt=0,lt=1,description="Give the confidence of the response.")
    category:str=Field(description="")
    keywords:list=Field(description="Give the keyword from the response")