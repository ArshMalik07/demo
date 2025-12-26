#Function Service-8:
# report_generator.py: It helps to generate brand visibility, brand mentions, persona visibility, 
#topic visibility & model visibility
from typing import Dict, List
from brand_scoring import score_brand_dimensions
from topic_scoring import score_topics
from persona_scoring import score_personas
from model_selection import get_model_config

def generate_final_report(company: str, category: str, topics: List[str], text_corpus: str) -> Dict:
    """
    Generates final structured analytics report as a JSON-compatible dict.
    """
    #  Brand Scoring
    brand_scores = score_brand_dimensions(company, category, text_corpus)
    # Topic Scoring 
    topic_scores = score_topics(company, category, topics, text_corpus)
    # Persona Scoring 
    persona_scores = score_personas(text_corpus)
    # Model visibility (always 100%, until another model integrated..) 
    model_cfg = get_model_config()
    model_visibility = {model_cfg.display_name: 100}

    # final JSON 
    report = {
        "brand_analysis": {
            "brand_visibility": brand_scores["brand_visibility"],
            "brand_mentions": brand_scores["brand_mentions"]
        },
        "persona_visibility": persona_scores,
        "topic_visibility": topic_scores,
        "model_visibility": model_visibility
    }

    return report