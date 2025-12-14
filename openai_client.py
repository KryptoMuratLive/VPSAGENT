# openai_client.py (GPT jetzt mit striktem Nur-Code-Prompt)
import openai
import os

def load_api_key():
    try:
        with open(".openai_key", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def generate_code_with_gpt(prompt: str, model="gpt-4"):
    api_key = load_api_key()
    if not api_key:
        raise Exception("OpenAI API-Key nicht gefunden.")

    client = openai.OpenAI(api_key=api_key)

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "Gib ausschließlich ausführbaren Python-Code in einem einzigen Markdown-Codeblock zurück (beginnend mit ```python). Keine Erklärungen, keine Einleitungen, keine Kommentare – nur lauffähiger Code."
                },
                {
                    "role": "user",
                    "content": f"{prompt}"
                }
            ],
            temperature=0.2,
            max_tokens=900
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Fehler bei der Code-Generierung: {str(e)}"
