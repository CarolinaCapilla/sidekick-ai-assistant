import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

# API keys and credentials
PUSHOVER_TOKEN = os.getenv("PUSHOVER_TOKEN")
PUSHOVER_USER = os.getenv("PUSHOVER_USER")
PUSHOVER_URL = "https://api.pushover.net/1/messages.json"

# Search API keys
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

# LLM settings
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gpt-4o-mini")

# Database settings
SQLITE_DB_FILE = os.getenv("SQLITE_DB_FILE", "sidekick_memory.sqlite")