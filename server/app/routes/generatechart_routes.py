from fastapi import APIRouter
from app.controllers.generatechart_controller import generate_chart


router = APIRouter()


@router.post("/generate-chart")
async def getChart(query: str, session_id: str):
    return await generate_chart(query, session_id)