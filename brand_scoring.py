# brand_scoring.py
from typing import Dict
import json
import re

from langchain_core.messages import HumanMessage
from llm_client import create_llm
from llm_utils import extract_text   # ✅ USE COMMON UTILITY


def extract_brand_mentions(company: str, category: str, text: str) -> Dict[str, int]:
    llm = create_llm()

    prompt = f"""
You are an intelligent competitive market analyst with expertise across multiple product categories.

Goal:
Find realistic competitor brands to "{company}" for category "{category}" from the text below.

TEXT:
{text}

Rules:
- Output must be ONLY a JSON object with key:value pairs
- Keys are brand names
- Values are integer competition scores (0-100), no decimals
- Include "{company}" itself
- Include only REAL competitor brands working in the SAME category
- Maximum 5 brands
- If no competitor identified, return {{}}
"""

    resp = llm.invoke([HumanMessage(content=prompt)])
    raw = extract_text(resp)   # ✅ SINGLE SOURCE OF TRUTH

    try:
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        competitors = json.loads(match.group(0)) if match else {}
    except:
        competitors = {}

    final_scores = {}
    for k, v in competitors.items():
        try:
            v = round(float(v))
        except:
            v = 0
        v = max(0, min(v, 100))  # clamp 0-100
        final_scores[k] = int(v)

    return final_scores


def calculate_brand_visibility(target_brand: str, brand_scores: Dict[str, int]):
    total = sum(brand_scores.values())
    if total == 0:
        return 0
    return round((brand_scores.get(target_brand, 0) / total) * 100)


def score_brand_dimensions(company: str, category: str, text: str) -> Dict[str, Dict[str, int]]:
    competitors = extract_brand_mentions(company, category, text)

    # STEP 1: Normalize keys to Title Case
    normalized = {}
    for brand, score in competitors.items():
        key = brand.strip().title()
        normalized[key] = normalized.get(key, 0) + score

    competitors = normalized

    # STEP 2: Ensure the main company exists
    company_name = company.strip().title()
    if company_name not in competitors:
        competitors[company_name] = 1

    # STEP 3: Compute visibility
    visibility_score = calculate_brand_visibility(company_name, competitors)

    return {
        "brand_visibility": {company_name: visibility_score},
        "brand_mentions": competitors
    }
