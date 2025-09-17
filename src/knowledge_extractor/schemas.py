from pydantic import BaseModel, Field
from typing import Optional, List


class TextInput(BaseModel):
    """
    Schema for text input to the /analyze endpoint.
    """
    text: str = Field(..., min_length=5, description="Unstructured text to analyze")


class AnalysisResponse(BaseModel):
    """
    Schema returned by both /analyze and /search endpoints.
    """
    id: int
    text: str
    summary: str
    title: Optional[str]
    topics: List[str]
    sentiment: str
    keywords: List[str]

    class Config:
        orm_mode = True
