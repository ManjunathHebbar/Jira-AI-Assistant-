import requests
import os

from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

load_dotenv()

JIRA_DOMAIN = os.getenv("JIRA_DOMAIN")
EMAIL = os.getenv("EMAIL")
API_TOKEN = os.getenv("API_TOKEN")


def add_ai_comment(issue_key, adf_content):

    url = (
        f"{JIRA_DOMAIN}"
        f"/rest/api/3/issue/"
        f"{issue_key}/comment"
    )

    payload = {
        "body": adf_content
    }

    response = requests.post(
        url,
        auth=HTTPBasicAuth(
            EMAIL,
            API_TOKEN
        ),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        json=payload
    )

    print(
        "COMMENT STATUS:",
        response.status_code
    )

    print(
        "COMMENT RESPONSE:",
        response.text
    )