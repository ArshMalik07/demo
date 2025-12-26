from pydantic import BaseModel
from typing import List, Optional


# ---------------------------
# Model selection (ONLY here)
# ---------------------------
class ModelRequest(BaseModel):
    model: str


# ---------------------------
# Requests
# ---------------------------
class CompanyRequest(BaseModel):
    url: str


class ProductRequest(BaseModel):
    company: str


class TopicRequest(BaseModel):
    company: str
    category: str


class PersonaRequest(BaseModel):
    persona: str


class PromptRequest(BaseModel):
    topic: str
    persona: str
    num: Optional[int] = 5


class AnalysisRequest(BaseModel):
    company: str
    category: str
    topics: List[str]
    persona: str
