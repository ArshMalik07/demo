from fastapi import FastAPI, HTTPException

# Schemas
from api.schemas import (
    ModelRequest,
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
from model_selection import set_model, get_model_config, model_config_dict


app = FastAPI(title="GEO Intelligence API")


# ---------------------------
# 1️⃣ Health Check
# ---------------------------
@app.get("/")
def read_root():
    return {"message": "Welcome to the GEO Intelligence API"}


# ---------------------------
# 2️⃣ MODEL SELECTION (ONCE)
# ---------------------------
@app.post("/select-model")
def select_model(req: ModelRequest):
    try:
        cfg = set_model(req.model)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid model. Use 'openai' or 'gemini'"
        )

    return {
        "message": "Model selected successfully",
        "active_model": cfg.provider,
        "display_name": cfg.display_name,
    }


# ---------------------------
# 3️⃣ URL → Company
# ---------------------------
@app.post("/company")
def get_company(req: CompanyRequest):
    company = get_company_if_valid(req.url)
    if not company:
        raise HTTPException(status_code=400, detail="Invalid or unknown domain")

    return {"company": company.title()}


# ---------------------------
# 4️⃣ Company → Products
# ---------------------------
@app.post("/products")
def get_products(req: ProductRequest):
    return extract_products(req.company)


# ---------------------------
# 5️⃣ Personas
# ---------------------------
@app.post("/personas")
def get_personas(req: TopicRequest):
    personas = generate_personas(
        company=req.company,
        category=req.category,
        num=6
    )

    if not personas:
        raise HTTPException(400, "Failed to generate personas")

    return {"personas": personas}


# ---------------------------
# 6️⃣ Category → Topics
# ---------------------------
@app.post("/topics")
def get_topics(req: TopicRequest):
    topics = generate_topics(
        company=req.company,
        selected_topic=req.category,
        num=6
    )
    return {"topics": topics}


# ---------------------------
# 7️⃣ Persona → Prompts
# ---------------------------
@app.post("/prompts")
def get_prompts(req: PromptRequest):
    prompts = generate_prompts(
        topic=req.topic,
        persona=req.persona,
        num=req.num
    )
    return {"prompts": prompts}


# ---------------------------
# 8️⃣ FINAL ANALYSIS
# ---------------------------
@app.post("/analyze")
def analyze(req: AnalysisRequest):

    prompts = generate_prompts(
        topic=req.category,
        persona=req.persona
    )

    if not prompts:
        raise HTTPException(400, "Failed to generate prompts")

    llm = create_llm()
    responses = []

    for _ in range(3):
        resp = llm.invoke([{"role": "user", "content": prompts[0]}])
        responses.append(resp.content)

    text_corpus = "\n\n".join(map(str, responses))

    report = generate_final_report(
        company=req.company,
        category=req.category,
        topics=req.topics,
        text_corpus=text_corpus
    )

    cfg = get_model_config()
    report["model_used"] = cfg.display_name

    return report
