from pydantic import BaseModel


class SummarizeText(BaseModel):
    link: str
