from typing import List
import re
import json

from langchain_core.messages import HumanMessage
from llm_client import create_llm
from llm_utils import extract_text   # ✅ IMPORT THIS


# -------------------------------
# Generate analytical prompts
# -------------------------------
def generate_prompts(topic: str, persona: str, num: int = 5) -> List[str]:

    persona_hints = {
        "founder": "strategic, funding, positioning, competitive moat",
        "product_manager": "roadmap prioritization, feature tradeoffs, user research, lifecycle",
        "marketing_analyst": "market trends, segmentation, demand drivers, messaging",
        "technical_lead": "architecture, reliability, scalability, performance bottlenecks",
        "investor": "ROI, TAM, competitive landscape, financial risk",
        "developer": "implementation details, APIs, debugging challenges",
        "designer": "UX, usability, accessibility, flow interactions",
        "researcher": "scientific analysis, measurable outcomes, study methodology",
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

    llm = create_llm()
    resp = llm.invoke([HumanMessage(content=prompt)])
    text = extract_text(resp)   # ✅ FIXED

    match = re.search(r"\[.*\]", text, re.DOTALL)
    return json.loads(match.group(0)) if match else []


# -------------------------------
# Generate topics
# -------------------------------
def generate_topics(company: str, selected_topic: str, num: int = 6) -> List[str]:
    prompt = f"""
Generate exactly {num} topic ideas.

Rules:
- Company: "{company}"
- Product category: "{selected_topic}"
- Topics should look like they would appear on research dashboards or business reports.
- Must be short and crisp (6–12 words ideally).
- NO academic long sentences.
- Should NOT start with Impact/Comparison/Exploration/Evaluation.
- No "how to" questions.
- No brand mentions.
- Purely LLM generative.

Return output as a JSON list only.
"""

    llm = create_llm()
    resp = llm.invoke([HumanMessage(content=prompt)])
    text = extract_text(resp)   # ✅ FIXED

    match = re.search(r"\[.*\]", text, re.DOTALL)
    try:
        return json.loads(match.group(0)) if match else []
    except:
        return []
