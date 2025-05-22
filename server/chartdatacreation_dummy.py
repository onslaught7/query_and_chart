import pandas as pd
import numpy as np
from typing import List, Dict, Any
from app.controllers.uploadfile_controller import user_sessions

def create_chart_data(session_id: str, chart_types: List[str], required_columns: List[List[str]]) -> Dict[str, Any]:
    """
    Create chart data for visualization based on LLM suggestions and preprocessed DataFrame.
    
    Args:
        session_id (str): Session ID to retrieve the DataFrame.
        chart_types (List[str]): List of chart types (e.g., ["bar", "pie"]).
        required_columns (List[List[str]]): List of column sets for each chart type.
    
    Returns:
        Dict[str, Any]: JSON-compatible dictionary with chart data and metadata, or error message.
    """
    # Validate session
    if session_id not in user_sessions:
        return {"error": "Invalid or expired session"}
    
    try:
        # Retrieve preprocessed DataFrame
        session_data = user_sessions[session_id]
        df = session_data["dataframe"]
        if df is None:
            return {"error": "No DataFrame available for this session"}
        
        # Validate inputs
        if len(chart_types) != len(required_columns):
            return {"error": "Mismatch between chart types and required columns"}
        
        # Define consistent colors for charts (theme-friendly for light/dark modes)
        colors = ["#36A2EB", "#FF6384", "#FFCE56", "#4BC0C0", "#9966FF", "#FF9F40"]

        # Output list for charts
        charts = []
        
        for chart_type, cols in zip(chart_types, required_columns):
            # Validate columns exist
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

            if chart_type == "bar":
                if len(cols) == 2:
                    # Aggregate: sum of numeric column by categorical/datetime column
                    if np.issubdtype(df[cols[1]].dtype, np.number):
                        grouped = df.groupby(cols[0])[cols[1]].sum().reset_index()
                    else:
                        return {"error": f"Column {cols[1]} must be numeric for bar chart"}
                    chart_data["data"] = {
                        "labels": grouped[cols[0]].astype(str).tolist(),  # Ensure strings for D3.js
                        "values": grouped[cols[1]].tolist()
                    }
                else:
                    # Count occurrences of categorical column
                    counts = df[cols[0]].value_counts().reset_index()
                    chart_data["data"] = {
                        "labels": counts[cols[0]].astype(str).tolist(),
                        "values": counts["count"].tolist()
                    }
                chart_data["metadata"]["title"] = f"{chart_data['metadata']['y_label']} by {chart_data['metadata']['x_label']}"

            elif chart_type == "pie":
                if len(cols) != 1:
                    return {"error": "Pie chart requires exactly one categorical column"}
                counts = df[cols[0]].value_counts().reset_index()
                chart_data["data"] = {
                    "labels": counts[cols[0]].astype(str).tolist(),
                    "values": counts["count"].tolist()
                }
                chart_data["metadata"]["title"] = f"Distribution of {chart_data['metadata']['x_label']}"

            elif chart_type == "line":
                if len(cols) != 2:
                    return {"error": "Line chart requires two columns (x: datetime/numeric, y: numeric)"}
                if not (np.issubdtype(df[cols[0]].dtype, np.datetime64) or np.issubdtype(df[cols[0]].dtype, np.number)):
                    return {"error": f"Column {cols[0]} must be datetime or numeric for line chart"}
                if not np.issubdtype(df[cols[1]].dtype, np.number):
                    return {"error": f"Column {cols[1]} must be numeric for line chart"}
                # Sort by x-axis for proper line rendering
                sorted_df = df.sort_values(cols[0])
                chart_data["data"] = {
                    "labels": sorted_df[cols[0]].astype(str).tolist(),  # Convert datetime to string
                    "values": sorted_df[cols[1]].tolist()
                }
                chart_data["metadata"]["title"] = f"{chart_data['metadata']['y_label']} over {chart_data['metadata']['x_label']}"

            elif chart_type == "scatter":
                if len(cols) != 2:
                    return {"error": "Scatter chart requires two numeric columns"}
                if not all(np.issubdtype(df[col].dtype, np.number) for col in cols):
                    return {"error": f"Columns {cols} must be numeric for scatter chart"}
                chart_data["data"] = {
                    "data": [{"x": x, "y": y} for x, y in zip(df[cols[0]], df[cols[1]])]
                }
                chart_data["metadata"]["title"] = f"{chart_data['metadata']['y_label']} vs {chart_data['metadata']['x_label']}"

            else:
                return {"error": f"Unsupported chart type: {chart_type}"}
            
            charts.append(chart_data)
        
        return {"charts": charts}
    
    except Exception as e:
        return {"error": f"Failed to create chart data: {str(e)}"}