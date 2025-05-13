from app.services.llm_service import query_gemini
from app.controllers.uploadfile_controller import user_sessions


def handle_user_query(query: str, session_id: str):
    try:
        text_file_content = user_sessions[session_id]["raw_text"]
        prompt = f"""
            The user has uploaded the following data: {text_file_content}
            You need to answer the following user query based on the uploaded data: {query} 
            Your answer should be cocise and to the point.
            Do not include any thing more than what is being asked by the user in the query or what is needed.
            You can include complete sentences though in you answers to give it a humanly touch.
        """
        response = query_gemini(prompt)
        print("----------------------The response received from the llm for user data and query----------------------")
        print(response)
        print("------------------------------------------------------------------------------------------------------")
        return {"response": response}
    except Exception as e:
        return {"error": str(e)}