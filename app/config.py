import os
from dotenv import load_dotenv

load_dotenv()

JIRA_DOMAIN = os.getenv("JIRA_DOMAIN")
EMAIL = os.getenv("JIRA_EMAIL")
API_TOKEN = os.getenv("JIRA_API_TOKEN")
PROJECT_KEY = os.getenv("PROJECT_KEY")
MAX_RESULTS = int(os.getenv("MAX_RESULTS", 50))
CUSTOM_FIELD_ID = os.getenv("CUSTOM_FIELD_ID")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")