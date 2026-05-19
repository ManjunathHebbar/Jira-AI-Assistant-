from app.ai.ollama_client import ask_ollama


def generate_ai_summary(title, description, comments):

    with open("app/prompts/summary.txt") as file:
        prompt_template = file.read()

    prompt = prompt_template.format(
        title=title,
        description=description,
        comments=comments
    )

    return ask_ollama(prompt)



def summarize_comments(comments):

    with open("app/prompts/comments.txt") as file:
        prompt_template = file.read()

    prompt = prompt_template.format(
        comments=comments
    )

    return ask_ollama(prompt)