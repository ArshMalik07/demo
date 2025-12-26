# test_run.py (CLI ONLY)
# Head of all functions – prints final analytics report

from extract_company import get_company_if_valid
from product_extractor import extract_products
from prompt_generator import generate_prompts, generate_topics
from personas import PERSONA_NAMES
from model_selection import set_model, get_model_config
from llm_client import create_llm
from report_generator import generate_final_report


# -------------------------------
# INTERNAL: COLLECT MULTIPLE RESPONSES
# -------------------------------
def collect_responses(prompt: str, num_samples: int = 5):
    llm = create_llm()
    responses = []

    for _ in range(num_samples):
        result = llm.invoke([{"role": "user", "content": prompt}])
        responses.append(result.content.strip())

    return responses


def combine_responses(responses):
    return "\n\n".join(responses)


# -------------------------------
# INTERNAL: PRETTY OUTPUT
# -------------------------------
def print_final_report(report: dict):
    print("\n--- FINAL REPORT ---")

    print("\nBrand Visibility:")
    for brand, score in report["brand_analysis"]["brand_visibility"].items():
        print(f"  {brand}: {score}%")

    print("\nBrand Mentions:")
    for brand, score in report["brand_analysis"]["brand_mentions"].items():
        print(f"  {brand}: {score}%")

    print("\nPersona Visibility:")
    for persona, score in report["persona_visibility"].items():
        print(f"  {persona}: {score}%")

    print("\nTopic Visibility:")
    for topic, score in report["topic_visibility"].items():
        print(f"  {topic}: {score}%")

    print("\nModel Visibility:")
    for model, score in report["model_visibility"].items():
        print(f"  {model}: {score}%")

    print("")


# ==================================================
# MAIN FLOW
# ==================================================

# -------------------------------
# STEP 0: MODEL SELECTION
# -------------------------------
print("\n--- MODEL SELECTION ---")
print("1. OpenAI (GPT-4o)")
print("2. Gemini (Flash)")

choice = input("Select model (1/2): ").strip()

if choice == "1":
    set_model("openai")
elif choice == "2":
    set_model("gemini")
else:
    print("Invalid model selection")
    exit()

cfg = get_model_config()
print(f"\nSelected Model: {cfg.display_name}")


# -------------------------------
# STEP 1: URL → COMPANY
# -------------------------------
url = input("\nEnter URL: ").strip()
company = get_company_if_valid(url)

if not company:
    print("\nDomain does NOT exist or invalid URL")
    exit()

company = company.strip().title()
print("\nCompany Name:", company)


# -------------------------------
# STEP 2: PRODUCT CATEGORIES
# -------------------------------
result = extract_products(company)
topics = result["topic"]

if not topics:
    print("\nNo topics found for this company.")
    exit()

print("\nTopics found:", topics)


# -------------------------------
# STEP 3: SELECT CATEGORY
# -------------------------------
selected_topic = input("\nSelect topic: ").strip()
if selected_topic not in topics:
    print("\nInvalid topic.")
    exit()

print("\nSelected Topic:", selected_topic)


# -------------------------------
# STEP 4: SELECT PERSONA
# -------------------------------
print("\nAvailable Personas:")
for p in PERSONA_NAMES:
    print(" -", p)

persona = input("\nEnter Persona: ").strip()
if persona not in PERSONA_NAMES:
    print("\nInvalid persona.")
    exit()

print("\nSelected Persona:", persona)


# -------------------------------
# STEP 5: GENERATE SUB-TOPICS
# -------------------------------
print("\n--- GENERATED TOPICS ---")
generated_topics = generate_topics(company, selected_topic, num=6)
for t in generated_topics:
    print("-", t)


# -------------------------------
# STEP 6: GENERATE PROMPTS
# -------------------------------
print("\n--- GENERATED PROMPTS ---")
prompts = generate_prompts(selected_topic, persona)
for p in prompts:
    print("-", p)


# -------------------------------
# STEP 7: COLLECT RESPONSES
# -------------------------------
first_prompt = prompts[0]
responses = collect_responses(first_prompt, num_samples=5)
full_text_corpus = combine_responses(responses)


# -------------------------------
# STEP 8: FINAL REPORT
# -------------------------------
report = generate_final_report(
    company,
    selected_topic,
    generated_topics,
    full_text_corpus
)


# -------------------------------
# STEP 9: OUTPUT
# -------------------------------
print_final_report(report)
