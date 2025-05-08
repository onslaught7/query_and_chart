from fastapi import APIRouter
from app.services.query_service import handle_user_query
from app.controllers.uploadfile_controller import user_sessions


router = APIRouter()


@router.post("/query-file")
async def queryFile(query: str, session_id: str):
    return await handle_user_query(query, session_id)