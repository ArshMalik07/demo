from fastapi import FastAPI, HTTPException
import socket
from urllib.parse import urlparse

# Schemas
from api.schemas import (
    CompanyRequest,
    ProductRequest,
    TopicRequest,
    PromptRequest,
    AnalysisRequest,
)

# Core services
from extract_company import get_company_if_valid
from product_extractor import extract_products
from prompt_generator import generate_prompts, generate_topics
from report_generator import generate_final_report
from personas import generate_personas
from llm_client import create_llm

app = FastAPI(title="GEO Intelligence API")


# ---------------------------
# 1️⃣ URL → Company
# ---------------------------

@app.get("/")
def read_root():
    return {"message": "Welcome to the GEO Intelligence API"}

@app.post("/company")
def get_company(req: CompanyRequest):
    company = get_company_if_valid(req.url)
    if not company:
        raise HTTPException(status_code=400, detail="Invalid or unknown domain")

    return {"company": company.title()}


# ---------------------------
# 2️⃣ Company → Products
# ---------------------------
@app.post("/products")
def get_products(req: ProductRequest):
    """
    Input:
    {
      "company": "Samsung"
    }
    """
    return extract_products(req.company)


# ---------------------------
# 3️⃣ Personas (static)
# ---------------------------
@app.post("/personas")
def get_personas(req: TopicRequest):
    """
    Input:
    {
      "company": "Samsung",
      "category": "Smartphones"
    }
    """
    personas = generate_personas(
        company=req.company,
        category=req.category,
        num=6
    )

    if not personas:
        raise HTTPException(400, "Failed to generate personas")

    return {"personas": personas}

# ---------------------------
# 4️⃣ Category → Topics
# ---------------------------
@app.post("/topics")
def get_topics(req: TopicRequest):
    """
    Input:
    {
      "company": "Samsung",
      "category": "Smartphones"
    }
    """
    topics = generate_topics(
        company=req.company,
        selected_topic=req.category,
        num=6
    )
    return {"topics": topics}


# ---------------------------
# 5️⃣ Persona → Prompts
# ---------------------------
@app.post("/prompts")
def get_prompts(req: PromptRequest):
    """
    Input:
    {
      "topic": "Smartphones",
      "persona": "designer"
    }
    """
    prompts = generate_prompts(
        topic=req.topic,
        persona=req.persona,
        num = req.num
    )
    return {"prompts": prompts}


# ---------------------------
# 6️⃣ FINAL ANALYSIS
# ---------------------------
@app.post("/analyze")
def analyze(req: AnalysisRequest):
    """
    Input:
    {
      "company": "Samsung",
      "category": "Smartphones",
      "persona": "designer",
      "topics": [...]
    }
    """

    # 1️⃣ Generate prompts
    prompts = generate_prompts(
        topic=req.category,
        persona=req.persona
    )

    if not prompts:
        raise HTTPException(status_code=400, detail="Failed to generate prompts")

    # 2️⃣ Collect LLM responses
    llm = create_llm()
    responses = []

    for _ in range(3):
        resp = llm.invoke([
            {"role": "user", "content": prompts[0]}
        ])
        responses.append(resp.content)

    text_corpus = "\n\n".join(responses)

    # 3️⃣ Generate report
    report = generate_final_report(
        company=req.company,
        category=req.category,
        topics=req.topics,
        text_corpus=text_corpus
    )

    return report
