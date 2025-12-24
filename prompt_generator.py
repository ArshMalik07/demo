# # Function Service-4
# # prompt_generator.py: Generate prompts based on selected persona & model

# from typing import List
# import json
# import re

# from langchain_core.messages import HumanMessage
# from llm_client import create_llm


# # -------------------------------------------------
# # Generate analytical prompts by persona
# # -------------------------------------------------
# def generate_prompts(
#     topic: str,
#     persona: str,
#     model_key: str,
#     num: int = 5
# ) -> List[str]:
#     """
#     Generates persona-aware analytical prompts using selected LLM
#     """

#     persona_hints = {
#         "founder": "strategic, funding, positioning, competitive moat",
#         "product_manager": "roadmap prioritization, feature tradeoffs, user research, lifecycle",
#         "marketing_analyst": "market trends, segmentation, demand drivers, messaging",
#         "technical_lead": "architecture, reliability, scalability, performance bottlenecks",
#         "investor": "ROI, TAM, competitive landscape, financial risk",
#         "developer": "implementation details, APIs, debugging challenges",
#         "designer": "UX, usability, accessibility, flow interactions",
#         "researcher": "scientific analysis, measurable outcomes, study methodology",
#     }

#     persona_hint = persona_hints.get(
#         persona.lower(),
#         "analytical exploration"
#     )

#     prompt = f"""
# Generate exactly {num} highly analytical prompts.

# Rules:
# - Persona: "{persona}"
# - Thinking Style: {persona_hint}
# - Topic: "{topic}"
# - Each prompt must be 1 sentence
# - No brand names
# - No generic filler
# - Clear, specific, insight-provoking
# - Must encourage analysis or evaluation

# Return ONLY a JSON list.
# """

#     llm = create_llm(model_key)
#     resp = llm.invoke([HumanMessage(content=prompt)])
#     text = resp.content.strip()

#     match = re.search(r"\[.*\]", text, re.DOTALL)
#     try:
#         return json.loads(match.group(0)) if match else []
#     except Exception:
#         return []


# # -------------------------------------------------
# # Generate research-style topics
# # -------------------------------------------------
# def generate_topics(
#     company: str,
#     selected_topic: str,
#     model_key: str,
#     num: int = 6
# ) -> List[str]:
#     """
#     Generates research-style topics using selected LLM
#     """

#     prompt = f"""
# Generate exactly {num} topic ideas.

# Rules:
# - Company: "{company}"
# - Product category: "{selected_topic}"
# - Topics should look like research dashboard labels
# - Short & crisp (6–12 words)
# - No brand mentions
# - No templates ("Impact", "Comparison", etc.)
# - Output ONLY a JSON list
# """

#     llm = create_llm(model_key)
#     resp = llm.invoke([HumanMessage(content=prompt)])
#     text = resp.content.strip()

#     match = re.search(r"\[.*\]", text, re.DOTALL)
#     try:
#         return json.loads(match.group(0)) if match else []
#     except Exception:
#         return []


#Function Service-4:
#prompt_generator.py: generate the prompts based on selected persona

import os
from typing import List
from dotenv import load_dotenv
import re
import json
load_dotenv()
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage

#.env
AZURE_BASE = os.getenv("AZURE_OPENAI_API_BASE") or "https://conversationalanalytics.openai.azure.com/"
AZURE_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")
AZURE_MODEL = os.getenv("AZURE_MODEL", "gpt-4o")

def get_llm():
    return AzureChatOpenAI(
        azure_endpoint=AZURE_BASE,
        model=AZURE_MODEL,
        openai_api_key=AZURE_KEY,
        openai_api_version=AZURE_VERSION,
        temperature=0.0
    )

# this fun generates the prompts by LLM
def generate_prompts(topic: str, persona: str, num: int = 5) -> List[str]:

    persona_hints = {
        "founder": "strategic, funding, positioning, competitive moat",
        "product_manager": "roadmap prioritization, feature tradeoffs, user research, lifecycle",
        "marketing_analyst": "market trends, segmentation, demand drivers, messaging",
        "technical_lead": "architecture, reliability, scalability, performance bottlenecks",
        "investor": "ROI, TAM, competitive landscape, financial risk",
        "developer": "implementation details, APIs, debugging challenges",
        "designer": "UX, usability, accessibility, flow interactions",
        "researcher": "scientific analysis, measurable outcomes, study methodology"
    }

    persona_hint = persona_hints.get(persona.lower(), "analytical exploration")

    prompt = f"""
Generate exactly {num} highly analytical prompts.

Rules:
- Persona: "{persona}"
- Thinking Style: {persona_hint}
- Topic: "{topic}"
- Each prompt must be 1 sentence.
- No brand names.
- No generic filler.
- No buzzwords without reasoning.
- Clear, specific, insight-provoking.
- Must encourage exploration, analysis, or evaluation.


Return ONLY a JSON list.
"""

    llm = get_llm()
    resp = llm.invoke([HumanMessage(content=prompt)])
    text = resp.content.strip()

    import json, re
    match = re.search(r"\[.*\]", text, re.DOTALL)
    return json.loads(match.group(0)) if match else []

#this fun generate topics(def=6)
def generate_topics(company: str, selected_topic: str, num: int = 6) -> List[str]:
    prompt = f"""
Generate exactly {num} topic ideas.

Rules:
- Company: "{company}"
- Product category: "{selected_topic}"
- Topics should look like they would appear on research dashboards or business reports.
- Must be short and crisp (6–12 words ideally).
- NO academic long sentences.
- Should NOT start with Impact/Comparison/Exploration/Evaluation (avoid templates).
- No "how to" guidance questions.
- No brand mentions on the generated topics.
- Must be purely LLM generative.

Examples pattern (NOT to copy, just to understand brevity):
"Energy Efficient Smart Home Devices"
"Smart TVs with Voice Assistant Integration"
"Best Smart TVs for Streaming"

Return output as a JSON list only.
"""

    llm = get_llm()
    resp = llm.invoke([HumanMessage(content=prompt)])
    text = resp.content.strip()

    # Extract JSON list
    match = re.search(r"\[.*\]", text, re.DOTALL)
    try:
        return json.loads(match.group(0)) if match else []
    except:
        return []