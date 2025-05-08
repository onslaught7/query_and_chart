from app.services.llm_service import query_gemini


prompt="Give me 5 steps of healthy life"
print(query_gemini(prompt))


async def handle_query(query: str):
    pass