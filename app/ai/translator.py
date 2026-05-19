from app.ai.ollama_client import ask_ollama


def translate_content(title, description):

    with open("app/prompts/translation.txt") as file:
        prompt_template = file.read()

    prompt = prompt_template.format(
        title=title,
        description=description
    )

    return ask_ollama(prompt)