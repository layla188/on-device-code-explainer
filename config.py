import os
from dotenv import load_dotenv

# ==========================
# Load Environment Variables
# ==========================
load_dotenv()


# ==========================
# Mode
# ==========================
# True  -> Local Ollama
# False -> Hosted OpenRouter
USE_LOCAL = True


# ==========================
# Local Ollama Configuration
# ==========================
LOCAL_MODEL = "qwen2.5-coder:0.5b"
LOCAL_BASE_URL = "http://localhost:11434/v1"

# ==========================
# Hosted OpenRouter
# ==========================
HOSTED_BASE_URL = "https://openrouter.ai/api/v1"

HOSTED_API_KEY = os.getenv("OPENROUTER_API_KEY")

HOSTED_MODEL = os.getenv(
    "MODEL_NAME",
    "openrouter/free"
)