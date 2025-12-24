# # Function Service-9
# # model_selection.py: Centralized model configuration & selection

# from dataclasses import dataclass
# import os
# from dotenv import load_dotenv

# # Load environment variables from .env
# load_dotenv()


# # -----------------------------
# # Model Config Dataclass
# # -----------------------------
# @dataclass
# class ModelConfig:
#     display_name: str
#     model_name: str          # deployment name (Azure) OR model id (Gemini)
#     api_version: str
#     temperature: float
#     max_tokens: int
#     provider: str            # "openai" | "gemini"


# # -----------------------------
# # OpenAI / Azure GPT-4o
# # -----------------------------
# OPENAI_GPT4O = ModelConfig(
#     display_name="OpenAI ChatGPT - GPT-4o",
#     model_name=os.getenv("AZURE_MODEL") or "gpt-4o",
#     api_version=os.getenv("AZURE_OPENAI_API_VERSION") or "2024-02-01-preview",
#     temperature=0.0,
#     max_tokens=2000,
#     provider="openai",
# )


# # -----------------------------
# # Google Gemini 2.5 Flash
# # -----------------------------
# GEMINI_25_FLASH = ModelConfig(
#     display_name="Google Gemini 2.5 Flash",
#     model_name=os.getenv("GEMINI_MODEL") or "gemini-2.5-flash",
#     api_version=os.getenv("GEMINI_API_VERSION") or "v1",
#     temperature=0.2,
#     max_tokens=2048,
#     provider="gemini",
# )


# # -----------------------------
# # Model Registry (INTERNAL KEYS)
# # -----------------------------
# MODEL_REGISTRY = {
#     "gpt4o": OPENAI_GPT4O,
#     "gemini_flash": GEMINI_25_FLASH,
# }


# # -----------------------------
# # User-facing name → internal key
# # -----------------------------
# MODEL_NAME_TO_KEY = {
#     "gpt-4o": "gpt4o",
#     "gemini-2.5-flash": "gemini_flash",
# }


# # -----------------------------
# # Resolver (MOST IMPORTANT)
# # -----------------------------
# def resolve_model_key(user_input: str) -> str:
#     """
#     Converts user input (model name or key)
#     to internal model_key used by the system
#     """
#     user_input = user_input.strip()

#     # Already a valid internal key
#     if user_input in MODEL_REGISTRY:
#         return user_input

#     # User-facing model name
#     if user_input in MODEL_NAME_TO_KEY:
#         return MODEL_NAME_TO_KEY[user_input]

#     raise ValueError(
#         f"Invalid model. Supported models: {list(MODEL_NAME_TO_KEY.keys())}"
#     )


# # -----------------------------
# # Public Helpers
# # -----------------------------
# def get_model_config(model_key: str = "gpt4o") -> ModelConfig:
#     """
#     Returns ModelConfig based on internal model_key
#     """
#     if model_key not in MODEL_REGISTRY:
#         raise ValueError(
#             f"Unknown model '{model_key}'. "
#             f"Available models: {list(MODEL_REGISTRY.keys())}"
#         )
#     return MODEL_REGISTRY[model_key]


# def model_config_dict(model_key: str = "gpt4o") -> dict:
#     """
#     Returns model config as dict (API / logging safe)
#     """
#     cfg = get_model_config(model_key)
#     return {
#         "model_key": model_key,
#         "display_name": cfg.display_name,
#         "model_name": cfg.model_name,
#         "api_version": cfg.api_version,
#         "temperature": cfg.temperature,
#         "max_tokens": cfg.max_tokens,
#         "provider": cfg.provider,
#     }


# def list_available_models() -> dict:
#     """
#     Returns all supported models
#     """
#     return {
#         key: model_config_dict(key)
#         for key in MODEL_REGISTRY
#     }





#Function Service-9:
# model_selection.py: It selects the fixed model
from dataclasses import dataclass
import os
from dotenv import load_dotenv
load_dotenv()

@dataclass
class ModelConfig:
    display_name: str
    azure_model: str
    api_version: str
    temperature: float
    max_tokens: int

# FIXED SINGLE MODEL 
OPENAI_GPT4O = ModelConfig(
    display_name="OpenAI ChatGPT - gpt4o",
    azure_model=os.getenv("AZURE_MODEL") or "gpt-4o",
    api_version=os.getenv("AZURE_OPENAI_API_VERSION") or "2024-02-01",
    temperature=0.0,
    max_tokens=2000,
)

def get_model_config() -> ModelConfig:
    return OPENAI_GPT4O

def model_config_dict() -> dict:
    cfg = OPENAI_GPT4O
    return {
        "display_name": cfg.display_name,
        "azure_model": cfg.azure_model,
        "api_version": cfg.api_version,
        "temperature": cfg.temperature,
        "max_tokens": cfg.max_tokens,
    }
