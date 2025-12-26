# personas.py
from typing import List
import json
import re

from langchain_core.messages import HumanMessage
from llm_client import create_llm
from llm_utils import extract_text   # ✅ COMMON NORMALIZER


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
    raw = extract_text(resp)   # ✅ SINGLE SOURCE OF TRUTH

    match = re.search(r"\[.*\]", raw, re.DOTALL)
    try:
        return json.loads(match.group(0)) if match else []
    except:
        return []
