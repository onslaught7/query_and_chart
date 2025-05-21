from app.controllers.uploadfile_controller import user_sessions
from app.services.query_service import handle_user_query
from app.config.llm_models import ModelName


async def query_handler(query: str, session_id: str, model: ModelName):
    if not session_id in user_sessions:
        return {"error": "Invalid or expired session"}
    else:
        return handle_user_query(query, session_id, model)