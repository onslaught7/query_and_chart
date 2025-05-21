from fastapi import APIRouter, Query
from app.controllers.query_controller import query_handler
from typing import List
from app.config.llm_models import ModelName


router = APIRouter()


@router.post("/query-file")
async def queryFile(
    query: str, 
    session_id: str, 
    model: ModelName = Query(..., description="Choose a model: chatgpt or gemini")):
    return await query_handler(query, session_id, model)