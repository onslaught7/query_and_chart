from json import JSONDecodeError

async def generate_chart(query: str, session_id: str, model: ModelName) -> Dict[str, Any]:
    if session_id not in user_sessions:
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
        Return only a JSON object with 'chart_types' and 'required_columns'.
        {
            "chart_types": ["bar", "pie"],
            "required_columns": [["ColumnA", "ColumnB"], ["ColumnX"]]
        }
        """
        user_prompt = f"""
        User Query: {query}
        Available Columns: {column_names}
        """
        full_prompt = system_prompt + "\n\n" + user_prompt

        if model == ModelName.chatgpt:
            response = query_gpt(full_prompt)
        elif model == ModelName.gemini:
            response = query_gemini(full_prompt)

        result = sanitize_llm_json(response)
        print(f"LLM Response for chart generation: {result}")

        # Create chart data
        chart_data = create_chart_data(session_id, result["chart_types"], result["required_columns"])
        return chart_data

    except JSONDecodeError as e:
        return {"error": f"LLM returned invalid JSON: {str(e)}"}
    except Exception as e:
        return {"error": str(e)}