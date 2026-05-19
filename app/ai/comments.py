from app.ai.ollama_client import ask_ollama



def summarize_comments(comments):

    prompt = f"""
Summarize these Jira comments into short actionable points.

Rules:
- Keep it concise
- Mention blockers/issues only
- Return bullet points

COMMENTS:
{comments}
"""

    return ask_ollama(prompt)