from pydantic import BaseModel
from typing import List, Dict, Optional


class ModelRequest(BaseModel):
    model: str

class CompanyRequest(BaseModel):
    url: str

class ProductRequest(BaseModel):
    company: str
    
class PersonaRequest(BaseModel):
    persona: str
class TopicRequest(BaseModel):
    company: str
    category: str

class PromptRequest(BaseModel):
    topic: str
    persona: str
    num: Optional[int] = 5 

class AnalysisRequest(BaseModel):
    company: str
    category: str
    topics: List[str]
    persona: str