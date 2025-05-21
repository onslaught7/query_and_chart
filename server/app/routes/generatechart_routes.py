from fastapi import APIRouter, Query
from app.controllers.generatechart_controller import generate_chart
from app.config.llm_models import ModelName


router = APIRouter()


@router.post("/generate-chart")
async def getChart(
    query: str, 
    session_id: str, 
    model: ModelName = Query(..., description="Choose a model: chatgpt or gemini")
    ):
    return await generate_chart(query, session_id, model)