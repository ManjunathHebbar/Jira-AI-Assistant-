import ollama

from app.config import OLLAMA_MODEL


def ask_ollama(prompt):

    try:

        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]

    except Exception as e:

        print("Ollama Error:", e)

        return "AI generation failed"
