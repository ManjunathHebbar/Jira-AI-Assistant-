import requests
import os

from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

load_dotenv()

JIRA_DOMAIN = os.getenv("JIRA_DOMAIN")
EMAIL = os.getenv("EMAIL")
API_TOKEN = os.getenv("API_TOKEN")



def fetch_issue_by_key(issue_key):

    url = f"{JIRA_DOMAIN}/rest/api/3/issue/{issue_key}"

    response = requests.get(
        url,
        auth=HTTPBasicAuth(EMAIL, API_TOKEN),
        headers={
            "Accept": "application/json"
        }
    )

    return response.json()