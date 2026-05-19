import requests
import os

from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

load_dotenv()

JIRA_DOMAIN = os.getenv("JIRA_DOMAIN")
EMAIL = os.getenv("EMAIL")
API_TOKEN = os.getenv("API_TOKEN")
CUSTOM_FIELD_ID = os.getenv("CUSTOM_FIELD_ID")



def update_custom_field(issue_key, content):

    url = f"{JIRA_DOMAIN}/rest/api/3/issue/{issue_key}"

    payload = {
        "fields": {
            CUSTOM_FIELD_ID: {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": str(content)[:30000]
                            }
                        ]
                    }
                ]
            }
        }
    }

    response = requests.put(
        url,
        auth=HTTPBasicAuth(EMAIL, API_TOKEN),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        json=payload
    )

    print(response.status_code)
    print("UPDATE STATUS:", response.status_code)
    print("UPDATE RESPONSE:", response.text)