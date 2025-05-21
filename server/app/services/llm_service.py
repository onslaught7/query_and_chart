from app.config.environment_config import settings
from google import genai
from google.genai import types
import openai


GEMINI_API_KEY = settings.GEMINI_API_KEY
OPENAI_API_KEY = settings.OPENAI_API_KEY
GEMINI_LLM_MODEL = settings.GEMINI_LLM_MODEL
OPENAI_LLM_MODEL = settings.OPENAI_LLM_MODEL


def query_gemini(prompt):
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        response = client.models.generate_content(
            model=GEMINI_LLM_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.4
            )
        )
        return response.text
    except Exception as e:
        print(f"An unexpected error occured: {e}")


def query_gpt(prompt):
    try:
        response = openai.chat.completions.create(
            model=OPENAI_LLM_MODEL,
            messages=[
                {"role": "system", "content": "You are a professional analyst who returns accurate, concise and detailed response to queries"},
                {"role": "user", "content": prompt},
            ],
            temperature=0
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"An unexpected error occured: {e}")