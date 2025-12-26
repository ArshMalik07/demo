# Function Service-2
# product_extractor.py: Extract products based on user input

import json
import re
from typing import List, Dict

from langchain_core.messages import HumanMessage
from llm_client import create_llm
from llm_utils import extract_text   # ✅ SINGLE SOURCE


# -------------------------------
# Product extraction
# -------------------------------
def llm_extract_products(company: str) -> List[str]:
    prompt = f"""
Identify whether "{company}" is:
1) A real company/brand
2) A material, product type, or industry category

Return a JSON list of real product categories.

Rules:
- If unknown or invalid → return []
- Do NOT hallucinate
- Output ONLY JSON LIST
"""

    llm = create_llm()
    resp = llm.invoke([HumanMessage(content=prompt)])
    raw = extract_text(resp)

    try:
        match = re.search(r"\[.*\]", raw, re.DOTALL)
        return json.loads(match.group(0)) if match else []
    except:
        return []


# -------------------------------
# Normalize categories
# -------------------------------
def normalize(categories: List[str]) -> List[str]:
    cleaned = []
    for c in categories:
        c = c.strip().lower()
        c = re.sub(r"[^a-zA-Z0-9\s]", "", c)
        if len(c) > 2:
            cleaned.append(c.title())
    return list(dict.fromkeys(cleaned))


# -------------------------------
# Public API
# -------------------------------
def extract_products(company: str) -> Dict[str, List[str]]:
    if not company or len(company) < 2:
        return {"topic": []}

    categories = llm_extract_products(company)
    return {"topic": normalize(categories)}


# -------------------------------
# Generate analytical topics
# -------------------------------
def generate_topics(selected_category: str, company: str) -> List[str]:
    prompt = f"""
Generate 5 analytical consumer-interest topics for category "{selected_category}"
under brand "{company}".

Rules:
- Research-worthy
- No product model names
- Output ONLY JSON LIST
"""

    llm = create_llm()
    resp = llm.invoke([HumanMessage(content=prompt)])
    raw = extract_text(resp)

    try:
        match = re.search(r"\[.*\]", raw, re.DOTALL)
        return json.loads(match.group(0)) if match else []
    except:
        return []
