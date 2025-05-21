from app.controllers.uploadfile_controller import user_sessions
from app.services.llm_service import query_gemini
from json import JSONDecodeError
import json


def sanitize_llm_json(raw_response: str) -> dict:
    cleaned = raw_response.strip()
    if cleaned.startswith("```"):
        cleaned = "\n".join(cleaned.splitlines()[1:-1])
    cleaned = cleaned.replace("```json", "").replace("```", "").strip()
    return json.loads(cleaned)


def preprocess_dataframe():
    # It is going to include a complete cleaning analogy of everything that is required to be done in the EDA step of cleaning
    pass


async def generate_chart(query: str, session_id: str = None):
    if not session_id in user_sessions:
        return {"error": "Invalid or expired session"}

    try:
        session_data = user_sessions[session_id]
        df = session_data["dataframe"]

        if df is None:
            return {"error": "No DataFrame available for this session"}
        
        column_names = df.columns.to_list()

        system_prompt = """
            You are a data visualization assistant. Based on the user's query and available data columns,
            suggest the best chart types and identify which columns are required for each chart.
            Strictly Return only a JSON object with 'chart_types' and 'required_columns'.
            Do NOT include markdown formatting (no triple backticks, no ```json).
            Strictly respond with a JSON object like: 
            {"chart_types": ["bar", "pie"], "required_columns": [["ColumnA", "ColumnB"], ["ColumnX"]]}'
            Each array in the array of required_columns corresponds to each chart type in the array of chart_types
             
        """
        user_prompt = f"""
            User Query: {query}\n
            Available Columns: {column_names}\n\n
            
        """
        full_prompt = system_prompt + "\n\n" + user_prompt

        response = query_gemini(full_prompt)
        print(f"Response from llm service: {response}")
        result = sanitize_llm_json(response)
        print(f"JSON Response for chart generation: {result}")
        # Logic to pass in the df and the columns required to a preprocess_dataframe for cleaning the dataframe for these particular columns
        # Passing this cleaned dataframe to the service chart_service and get the charts
        return result
    except JSONDecodeError as e:
        return {"error": f"LLM returned invalid JSON: {str(e)}"}
    except Exception as e:
        return {"error": str(e)}