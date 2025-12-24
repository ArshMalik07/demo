# # Function Service-10
# # llm_client.py: LLM factory for OpenAI (Azure) & Gemini

# import os
# from dotenv import load_dotenv

# from langchain_openai import AzureChatOpenAI
# from langchain_google_genai import ChatGoogleGenerativeAI

# from model_selection import get_model_config

# load_dotenv()


# def create_llm(model_key: str = "gpt4o"):
#     """
#     Factory function to create LLM based on model_key

#     Supported:
#     - Azure OpenAI (GPT-4o)
#     - Google Gemini (2.5 Flash)
#     """

#     cfg = get_model_config(model_key)

#     # -------------------------------------------------
#     # Azure OpenAI (GPT-4o)
#     # -------------------------------------------------
#     if cfg.provider == "openai":
#         azure_key = os.getenv("AZURE_OPENAI_API_KEY")
#         azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

#         if not azure_key or not azure_endpoint:
#             raise RuntimeError(
#                 "Missing Azure OpenAI credentials. "
#                 "Please set AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT."
#             )

#         return AzureChatOpenAI(
#             azure_deployment="gpt-4o",   
#             api_version=cfg.api_version,
#             temperature=cfg.temperature,
#             max_tokens=cfg.max_tokens,
#             azure_endpoint=azure_endpoint,
#             api_key=azure_key,
#         )

#     # -------------------------------------------------
#     # Google Gemini (2.5 Flash)
#     # -------------------------------------------------
#     elif cfg.provider == "gemini":
#         gemini_key = os.getenv("GEMINI_API_KEY")

#         if not gemini_key:
#             raise RuntimeError(
#                 "Missing GEMINI_API_KEY. "
#                 "Please set it in the .env file."
#             )

#         return ChatGoogleGenerativeAI(
#             model=cfg.model_name,
#             temperature=cfg.temperature,
#             max_output_tokens=cfg.max_tokens,
#             google_api_key=gemini_key,
#         )

#     # -------------------------------------------------
#     # Unsupported provider
#     # -------------------------------------------------
#     else:
#         raise ValueError(f"Unsupported provider: {cfg.provider}")



import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from model_selection import get_model_config
load_dotenv()

AZURE_BASE = os.getenv("AZURE_OPENAI_API_BASE") or "https://conversationalanalytics.openai.azure.com/"
AZURE_KEY = os.getenv("AZURE_OPENAI_API_KEY")

if not AZURE_KEY:
    raise RuntimeError("Missing Azure API key")

def create_llm():
    cfg = get_model_config()
    return AzureChatOpenAI(
        azure_endpoint=AZURE_BASE,
        model=cfg.azure_model,
        openai_api_key=AZURE_KEY,
        openai_api_version=cfg.api_version,
        temperature=cfg.temperature,
        max_tokens=cfg.max_tokens,
    )