# # Function Service-7
# # topic_scoring.py: Scores topic relevance using selected LLM

# from typing import Dict, List
# from llm_client import create_llm
# from langchain_core.messages import HumanMessage
# import json
# import re


# def score_topics(
#     company: str,
#     category: str,
#     topics: List[str],
#     text: str,
#     model_key: str
# ) -> Dict[str, int]:
#     """
#     Scores each topic from 0–100 based on relevance within the given text.
#     Returns: { topic: integer_score }
#     """

#     # 🔥 MODEL-AWARE LLM
#     llm = create_llm(model_key)

#     prompt = f"""
# Given this company: "{company}"
# And this product category: "{category}"

# Evaluate the relevance of each topic below, based on the text content.

# TEXT:
# {text}

# TOPICS:
# {json.dumps(topics)}

# Rules:
# - Return a JSON dict {{ "topic": score_integer }}
# - Score must be 0–100 (no decimals)
# - Higher score = stronger contextual relevance
# - Do NOT force scores to sum to 100
# """

#     resp = llm.invoke([HumanMessage(content=prompt)])
#     raw = resp.content.strip()

#     try:
#         match = re.search(r"\{.*\}", raw, re.DOTALL)
#         result = json.loads(match.group(0)) if match else {}
#     except Exception:
#         result = {}

#     # Post-process → clamp & int
#     cleaned = {}
#     for topic, score in result.items():
#         try:
#             score = round(float(score))
#         except Exception:
#             score = 0
#         score = max(0, min(score, 100))
#         cleaned[topic] = int(score)

#     return cleaned






#Function Service-7:
# topic_scoring.py: It scores the mentioned topics
from typing import Dict, List
from llm_client import create_llm
from langchain_core.messages import HumanMessage
import json
import re

def score_topics(company: str, category: str, topics: List[str], text: str) -> Dict[str, int]:
    """
    Scores each topic from 0-100 based on relevance within the given corpus text.
    Returns: { topic: integer_score }
    """
    llm = create_llm()

    prompt = f"""
Given this company: "{company}"
And this product category: "{category}"

Evaluate the relevance of each topic below, based on the text content:

TEXT:
{text}

TOPICS:
{json.dumps(topics)}

Rules:
- Return a JSON dict {{"topic": score_integer}} for each topic
- Score must be 0-100 (no decimals)
- Score indicates relevance strength (not probability)
- Do NOT force scores to sum to 100
- Higher score means stronger contextual relevance
- Lower score means weaker contextual relevance
    """

    resp = llm.invoke([HumanMessage(content=prompt)])
    raw = resp.content.strip()

    try:
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        result = json.loads(match.group(0)) if match else {}
    except:
        result = {}

    # Convert to rounded integer and clamp 0-100
    for k, v in result.items():
        try:
            v = round(float(v))
        except:
            v = 0
        v = max(0, min(v, 100))
        result[k] = int(v)

    return result
