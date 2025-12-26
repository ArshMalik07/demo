# model_selection.py
from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

# ------------------ Config ------------------

@dataclass
class ModelConfig:
    provider: str
    display_name: str
    azure_model: str | None
    api_version: str | None
    temperature: float
    max_tokens: int


# ------------------ Models ------------------

OPENAI_GPT4O = ModelConfig(
    provider="openai",
    display_name="OpenAI ChatGPT - GPT-4o",
    azure_model=os.getenv("AZURE_MODEL", "gpt-4o"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01"),
    temperature=0.0,
    max_tokens=2000,
)

GEMINI_FLASH = ModelConfig(
    provider="gemini",
    display_name="Gemini Flash",
    azure_model=None,
    api_version=None,
    temperature=0.0,
    max_tokens=2000,
)

# ------------------ GLOBAL STATE ------------------

_ACTIVE_MODEL: ModelConfig = OPENAI_GPT4O   # default


# ------------------ API ------------------

def set_model(provider: str) -> ModelConfig:
    global _ACTIVE_MODEL

    provider = provider.lower().strip()

    if provider == "openai":
        _ACTIVE_MODEL = OPENAI_GPT4O
    elif provider == "gemini":
        _ACTIVE_MODEL = GEMINI_FLASH
    else:
        raise ValueError("Invalid model")

    return _ACTIVE_MODEL


def get_model_config() -> ModelConfig:
    # ✅ ONLY read from runtime state
    return _ACTIVE_MODEL


def model_config_dict() -> dict:
    cfg = _ACTIVE_MODEL
    return {
        "provider": cfg.provider,
        "display_name": cfg.display_name,
        "temperature": cfg.temperature,
        "max_tokens": cfg.max_tokens,
    }
