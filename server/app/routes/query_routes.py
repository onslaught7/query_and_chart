from fastapi import APIRouter
from app.controllers.query_controller import query_handler


router = APIRouter()


@router.post("/query-file")
async def queryFile(query: str, session_id: str):
    return await query_handler(query, session_id)