# llm_client.py

import os
from dotenv import load_dotenv

from langchain_openai import AzureChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

from model_selection import get_model_config

# Load environment variables
load_dotenv()

# ---------- Azure OpenAI Config ----------
AZURE_BASE = os.getenv("AZURE_OPENAI_API_BASE") or "https://conversationalanalytics.openai.azure.com/"
AZURE_KEY = os.getenv("AZURE_OPENAI_API_KEY")

# ---------- Gemini Config ----------
GEMINI_KEY = os.getenv("GEMINI_API_KEY")


def create_llm():
    """
    Factory function to return an LLM client based on selected provider.
    Supported providers:
      - openai (Azure OpenAI)
      - gemini (Google Gemini Flash)
    """

    cfg = get_model_config()

    # ---------------- OpenAI (Azure) ----------------
    if cfg.provider == "openai":
        if not AZURE_KEY:
            raise RuntimeError("Missing AZURE_OPENAI_API_KEY")

        return AzureChatOpenAI(
            azure_endpoint=AZURE_BASE,
            model=cfg.azure_model,
            openai_api_key=AZURE_KEY,
            openai_api_version=cfg.api_version,
            temperature=cfg.temperature,
            max_tokens=cfg.max_tokens,
        )

    # ---------------- Gemini ----------------
    elif cfg.provider == "gemini":
        if not GEMINI_KEY:
            raise RuntimeError("Missing GEMINI_API_KEY")

        return ChatGoogleGenerativeAI(
            model="gemini-flash-latest",
            google_api_key=GEMINI_KEY,
            temperature=cfg.temperature,
            max_output_tokens=cfg.max_tokens,
        )

    # ---------------- Invalid Provider ----------------
    else:
        raise ValueError(f"Unsupported LLM provider: {cfg.provider}")
