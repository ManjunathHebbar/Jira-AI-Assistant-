from app.ai.ollama_client import ask_ollama


def analyze_sentiment(title, description, comments):

    with open("app/prompts/sentiment.txt") as file:
        prompt_template = file.read()

    prompt = prompt_template.format(
        title=title,
        description=description,
        comments=comments
    )

    return ask_ollama(prompt)