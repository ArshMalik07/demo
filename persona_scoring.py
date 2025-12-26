# Function Service-6
# persona_scoring.py: It scores the mentioned personas

from typing import Dict
import json
import re

from langchain_core.messages import HumanMessage
from llm_client import create_llm
from personas import generate_personas
from llm_utils import extract_text   # ✅ COMMON NORMALIZER


def score_personas(text: str) -> Dict[str, int]:
    """
    Scores each persona based on relevance in context.
    text = combined LLM responses / prompts context.
    Returns: { persona: integer_score }
    """
    llm = create_llm()

    personas = generate_personas("", "")

    prompt = f"""
Analyze the following text and evaluate how strongly each persona viewpoint appears:

TEXT:
{text}

Personas:
{json.dumps(personas)}

Rules:
- Score each persona from 0 to 100 (no decimals)
- Higher score = stronger textual relevance
- Lower score = weaker relevance
- Output must be ONLY a JSON object
"""

    resp = llm.invoke([HumanMessage(content=prompt)])
    raw = extract_text(resp)   # ✅ SINGLE SOURCE

    try:
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        result = json.loads(match.group(0)) if match else {}
    except:
        result = {}

    # Clamp + normalize
    final = {}
    for k, v in result.items():
        try:
            v = round(float(v))
        except:
            v = 0
        final[k] = max(0, min(v, 100))

    # Sort descending
    return dict(sorted(final.items(), key=lambda x: x[1], reverse=True))
