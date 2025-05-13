from app.controllers.uploadfile_controller import user_sessions
from app.services.query_service import handle_user_query


async def query_handler(query: str, session_id: str):
    if not session_id in user_sessions:
        return {"error": "Invalid or expired session"}
    else:
        return handle_user_query(query, session_id)