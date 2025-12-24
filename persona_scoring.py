#Function Service-6:
# persona_scoring.py: It scores the mentioned personas
from typing import Dict, List
from personas import generate_personas
from llm_client import create_llm
from langchain_core.messages import HumanMessage
import json
import re


def score_personas(text: str) -> Dict[str, int]:
    """
    Scores each persona based on relevance in context.
    text = combined LLM responses / prompts context.
    Returns: { persona: integer_score }
    """
    llm = create_llm()

    prompt = f"""
Analyze the following text and evaluate how strongly each persona viewpoint appears:

TEXT:
{text}

Personas:
{json.dumps(generate_personas("",""))}

Rules:
- Score each persona from 0 to 100 (no decimals)
- Higher score = stronger textual relevance to that persona
- Lower score = weaker relevance
- Output must be a JSON dict {{ "persona_name": score }}

Example output:
{{"technical_lead": 58, "investor": 32, ...}}
    """

    resp = llm.invoke([HumanMessage(content=prompt)])
    raw = resp.content.strip()

    try:
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        result = json.loads(match.group(0)) if match else {}
    except:
        result = {}

    # Post-process → integer & clamp 0–100
    for k, v in result.items():
        try:
            v = round(float(v))
        except:
            v = 0
        v = max(0, min(v, 100))
        result[k] = int(v)

    # Sort descending by score (persona relevance ranking)
    sorted_pairs = sorted(result.items(), key=lambda x: x[1], reverse=True)
    sorted_result = {k: v for k, v in sorted_pairs}

    return sorted_result