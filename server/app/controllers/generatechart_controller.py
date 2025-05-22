from app.controllers.uploadfile_controller import user_sessions
from app.services.llm_service import query_gemini, query_gpt
from app.services.chart_service import create_chart_data
from app.config.llm_models import ModelName
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


async def get_dataset_description(session_id: str, model: ModelName):
    if not session_id in user_sessions:
        return {"error": "Invalid or expired session"}
    
    try:
        session_data = user_sessions[session_id]
        raw_text = session_data["raw_text"]

        if raw_text is None:
            return {"error": "No DataFrame available for this session"}
        
        system_prompt = """
        You are a professional data analyst tasked with profiling datasets. 
        Your job is to:
        1. Give a **clean, human-readable title** for the dataset.
        2. Write a short **summary description** of what the dataset is about.
        3. Analyze all the columns and describe their meanings clearly.
        4. Detect column types: "numeric", "categorical", "datetime", or "text".

        Return your response **only** as a JSON object in this format:
        {
        "title": "Descriptive Title",
        "description": "Brief summary of the dataset",
        "columns": [
            {"name": "ColumnA", "type": "numeric", "description": "What this column means"},
            ...
        ]
        }

        Do not include markdown or any extra commentary and no triple backticks, no ```json. Output a valid JSON only.
        """

        user_prompt = f"""
        Here is the dataset:

        {raw_text}

        Analyze and describe it as instructed.
        """

        full_prompt = system_prompt + "\n\n" + user_prompt

        if model == ModelName.chatgpt:
            response = query_gpt(full_prompt)
        elif model == ModelName.gemini:
            response = query_gemini(full_prompt)

        print(f"Complete Description of the dataset: {response}")
        result = sanitize_llm_json(response)
        print(f"JSON Response description of the dataset: {result}")

        return result
    except JSONDecodeError as e:
        return {"error": f"LLM returned invalid JSON: {str(e)}"}
    except Exception as e:
        return {"error": str(e)}


async def generate_chart(query: str, session_id: str, model: ModelName):
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
        Strictly return only a JSON object with 'chart_types' and 'required_columns'.
        Do NOT include markdown formatting (no triple backticks, no ```json).
        Strictly respond with a JSON object like: 
        {"chart_types": ["bar", "pie"], "required_columns": [["ColumnA", "ColumnB"], ["ColumnX"]]}
        Each array in the array of required_columns corresponds to each chart type in the array of chart_types.

        When choosing columns for charts that require both x and y axes (e.g., bar, line, scatter),
        ensure that:
        - The x-axis column should be categorical or time-based (e.g., region, product, date).
        - The y-axis column should be quantitative/numeric (e.g., sales, revenue, profit, count).
        - The first column in each pair must represent the x-axis.
        - The second column in each pair must represent the y-axis.

        Use only the available data columns provided and avoid using invalid or duplicate column combinations.
        """

        user_prompt = f"""
            User Query: {query}\n
            Available Columns: {column_names}\n\n
            
        """
        full_prompt = system_prompt + "\n\n" + user_prompt

        if model == ModelName.chatgpt:
            response = query_gpt(full_prompt)
        elif model == ModelName.gemini:
            response = query_gemini(full_prompt)

        print(f"Response from llm service: {response}")
        result = sanitize_llm_json(response)
        print(f"JSON Response for chart generation: {result}")
        # Logic to pass in the df and the columns required to a preprocess_dataframe for cleaning the dataframe for these particular columns

        # Passing this cleaned dataframe to the service chart_service and get the charts
        chart_data = create_chart_data(session_id, result["chart_types"], result["required_columns"])
        return chart_data
    except JSONDecodeError as e:
        return {"error": f"LLM returned invalid JSON: {str(e)}"}
    except Exception as e:
        return {"error": str(e)}