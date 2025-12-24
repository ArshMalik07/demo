# persona_generator.py
from typing import List
from langchain_core.messages import HumanMessage
from llm_client import create_llm
import json, re


def generate_personas(company: str, category: str, num: int = 6) -> List[str]:
    """
    Generate context-aware personas using LLM
    """

    prompt = f"""
You are a market research expert.

Generate {num} realistic professional personas
who would actively analyze, evaluate, or influence
decisions in the domain below.

Company: {company}
Category: {category}

Rules:
- Personas must be real-world professional roles
- No generic words like "User" or "Customer"
- Should reflect business, technical, research & strategy viewpoints
- Each persona should be 2–5 words
- Output ONLY a JSON list
"""

    llm = create_llm()
    resp = llm.invoke([HumanMessage(content=prompt)])
    raw = resp.content.strip()

    match = re.search(r"\[.*\]", raw, re.DOTALL)
    return json.loads(match.group(0)) if match else []
