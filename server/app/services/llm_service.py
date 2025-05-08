from app.config.environment_config import settings
from google import genai
from google.genai import types


GEMINI_API_KEY = settings.GEMINI_API_KEY
LLM_MODEL = settings.LLM_MODEL


def query_gemini(prompt):
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        response = client.models.generate_content(
            model=LLM_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.4
            )
        )
        return response.text
    except Exception as e:
        print(f"An unexpected error occured: {e}")