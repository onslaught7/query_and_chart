import pandas as pd
import numpy as np
from typing import List, Dict, Any
from app.controllers.uploadfile_controller import user_sessions


def create_chart_data(session_id: str, chart_types: List[str], required_columns: List[List[str]]) -> Dict[str, Any]:
    if session_id not in user_sessions:
        return {"error": "Invalid or expired session"}
    
    try: 
        session_data = user_sessions[session_data]
        df = session_data["dataframe"]
        if df in None:
            return {"error": "No DataFrame available for this session"}
        
        if len(chart_types) != len(required_columns):
            return {"error": "Mismatch between chart types and required columns"}
        
        colors = ["#36A2EB", "#FF6384", "#FFCE56", "#4BC0C0", "#9966FF", "#FF9F40"]

        charts = [] # This list will contain the charts to be output

        for chart_type, cols in zip(chart_types, required_columns):
            if not all(col in df.columns for col in cols):
                return {"error": f"Columns {cols} not found in DataFrame. Available: {list(df.columns)}"}

            chart_data = {
                "chart_type": chart_type,
                "data": {},
                "metadata": {
                    "x_label": cols[0],
                    "y_label": cols[1] if len(cols) > 1 else "Count",
                    "colors": colors[:len(df[cols[0]].unique())] if cols[0] in df.columns else colors
                }
            }

    except Exception as e:
        return {"error": f"Failed to create chart data: {str(e)}"}