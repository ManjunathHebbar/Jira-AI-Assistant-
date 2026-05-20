import requests
from requests.auth import HTTPBasicAuth

from app.config import (
    API_TOKEN,
    EMAIL,
    JIRA_DOMAIN,
    require_settings
)



def fetch_issue_by_key(issue_key):

    require_settings(
        "JIRA_DOMAIN",
        "EMAIL",
        "API_TOKEN"
    )

    url = f"{JIRA_DOMAIN}/rest/api/3/issue/{issue_key}"

    response = requests.get(
        url,
        auth=HTTPBasicAuth(EMAIL, API_TOKEN),
        headers={
            "Accept": "application/json"
        },
        timeout=30
    )

    try:

        response.raise_for_status()

    except requests.HTTPError as error:

        raise RuntimeError(
            f"Failed to fetch Jira issue {issue_key}: "
            f"{response.status_code} {response.text}"
        ) from error

    return response.json()
