# # test_run.py (CLI ONLY)

# from extract_company import get_company_if_valid
# from product_extractor import extract_products
# from prompt_generator import generate_prompts, generate_topics
# from personas import PERSONA_NAMES
# from model_selection import resolve_model_key, get_model_config
# from llm_client import create_llm
# from report_generator import generate_final_report


# def main():
#     # -----------------------------
#     # STEP 0: MODEL SELECTION
#     # -----------------------------
#     model_input = input("Select model (gpt-4o/gemini-2.5-flash): ").strip()

#     try:
#         model_key = resolve_model_key(model_input)
#     except ValueError as e:
#         print(e)
#         return

#     cfg = get_model_config(model_key)
#     print(f"\nSelected Model: {cfg.display_name}")

#     # -----------------------------
#     # STEP 1: URL → COMPANY
#     # -----------------------------
#     url = input("\nEnter URL: ").strip()
#     company = get_company_if_valid(url)

#     if not company:
#         print("\nDomain does NOT exist or invalid URL")
#         return

#     company = company.strip().title()
#     print("\nCompany Name:", company)

#     # -----------------------------
#     # STEP 2: PRODUCT CATEGORIES
#     # -----------------------------
#     result = extract_products(company, model_key)
#     topics = result["topic"]

#     if not topics:
#         print("\nNo topics found for this company.")
#         return

#     print("\nTopics found:", topics)

#     # -----------------------------
#     # STEP 3: SELECT CATEGORY
#     # -----------------------------
#     selected_topic = input("\nSelect topic: ").strip()
#     if selected_topic not in topics:
#         print("\nInvalid topic.")
#         return

#     print("\nSelected Topic:", selected_topic)

#     # -----------------------------
#     # STEP 4: SELECT PERSONA
#     # -----------------------------
#     print("\nAvailable Personas:")
#     for p in PERSONA_NAMES:
#         print(" -", p)

#     persona = input("\nEnter Persona: ").strip()
#     if persona not in PERSONA_NAMES:
#         print("\nInvalid persona.")
#         return

#     print("\nSelected Persona:", persona)

#     # -----------------------------
#     # STEP 5: GENERATE TOPICS
#     # -----------------------------
#     print("\n--- GENERATED TOPICS ---")
#     generated_topics = generate_topics(
#         company,
#         selected_topic,
#         model_key,
#         num=6
#     )
#     for t in generated_topics:
#         print("-", t)

#     # -----------------------------
#     # STEP 6: GENERATE PROMPTS
#     # -----------------------------
#     prompts = generate_prompts(
#         selected_topic,
#         persona,
#         model_key
#     )

#     print("\n--- GENERATED PROMPTS ---")
#     for p in prompts:
#         print("-", p)

#     # -----------------------------
#     # STEP 7: COLLECT RESPONSES
#     # -----------------------------
#     llm = create_llm(model_key)
#     responses = [
#         llm.invoke([{"role": "user", "content": prompts[0]}]).content
#         for _ in range(3)
#     ]
#     full_text = "\n\n".join(responses)

#     # -----------------------------
#     # STEP 8: FINAL REPORT
#     # -----------------------------
#     report = generate_final_report(
#         company,
#         selected_topic,
#         generated_topics,
#         full_text,
#         model_key
#     )

#     print("\n--- FINAL REPORT ---")
#     print(report)


# if __name__ == "__main__":
#     main()


#test_run.py: Head of all functions which it prints the function's output
from extract_company import get_company_if_valid
from product_extractor import extract_products
from prompt_generator import generate_prompts, generate_topics
from personas import generate_personas
from model_selection import get_model_config
from llm_client import create_llm
from report_generator import generate_final_report

# INTERNAL: COLLECT MULTIPLE RESPONSES (not printed)
def collect_responses(prompt: str, num_samples: int = 5):
    llm = create_llm()
    res = []
    for _ in range(num_samples):
        result = llm.invoke([{"role": "user", "content": prompt}])
        res.append(result.content.strip())
    return res

def combine_responses(responses):
    return "\n\n".join(responses)

# INTERNAL: CLEAN OUTPUT
def print_final_report(report: dict):
    print("\n--- FINAL REPORT ---")

    # BRAND ANALYSIS
    print("\nBrand Visibility:")
    for brand, score in report["brand_analysis"]["brand_visibility"].items():
        print(f"  {brand}: {score}%")

    print("\nBrand Mentions:")
    for brand, score in report["brand_analysis"]["brand_mentions"].items():
        print(f"  {brand}: {score}%")

    # PERSONAS
    print("\nPersona Visibility:")
    for persona, score in report["persona_visibility"].items():
        print(f"  {persona}: {score}%")

    # TOPICS 
    print("\nTopic Visibility:")
    for topic, score in report["topic_visibility"].items():
        print(f"  {topic}: {score}%")

    # MODEL 
    print("\nModel Visibility:")
    for model, score in report["model_visibility"].items():
        print(f"  {model}: {score}%")

    print("")

# STEP 1: URL → COMPANY
url = input("Enter URL: ").strip()
company = get_company_if_valid(url)

if not company:
    print("\nDomain does NOT exist or invalid URL")
    exit()

#this helps to uppercase the 1st letter of input
original_company = company.strip().title()
print("\nCompany Name:", original_company)

# STEP 2: PRODUCT CATEGORIES
result = extract_products(company)
topics = result["topic"]

if not topics:
    print("\nNo topics found for this company.")
    exit()

print("\nTopics found:", topics)

# STEP 3: SELECT CATEGORY
selected_topic = input("\nSelect topic: ").strip()
if selected_topic not in topics:
    print("\nInvalid topic.")
    exit()

print("\nSelected Topic:", selected_topic)

# STEP 4: SELECT PERSONA
print("\nAvailable Personas:")
for p in PERSONA_NAMES:
    print(" -", p)

persona = input("\nEnter Persona: ").strip()
if persona not in PERSONA_NAMES:
    print("\nInvalid persona.")
    exit()

print("\nSelected Persona:", persona)

# STEP 5: GENERATE SUB-TOPICS
print("\n--- GENERATED TOPICS ---")
generated_topics = generate_topics(company, selected_topic, num=6)
for t in generated_topics:
    print("-", t)

# STEP 6: GENERATE PROMPTS
prompts = generate_prompts(selected_topic, persona)

print("\n--- GENERATED PROMPTS ---")
for p in prompts:
    print("-", p)

# STEP 7: SELECT MODEL
print("\n--- MODEL SELECTION ---")
model_input = input("Select Model name: ").strip().lower()

if model_input != "gpt-4o":
    print("\nInvalid model. Only 'gpt-4o' is supported.")
    exit()

cfg = get_model_config()
print(f"\nSelected Model: {cfg.display_name}")

# STEP 8: COLLECT 5 INTERNAL RESPONSES
first_prompt = prompts[0]               # use first prompt
responses = collect_responses(first_prompt, num_samples=5)
full_text_corpus = combine_responses(responses)

# STEP 9: SCORING + FINAL REPORT
report = generate_final_report(company, selected_topic, generated_topics, full_text_corpus)

# STEP 10: PRETTY OUTPUT
print_final_report(report)
