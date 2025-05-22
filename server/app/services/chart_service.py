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

            if chart_type == "bar":
                if len(cols) == 2:
                    if np.issubdtype(df[cols[1]].dtype, np.number):
                        grouped = df.groupby(cols[0])[cols[1].sum().reset_index]
                    else:
                        return {"error": f"Column {cols[1]} must be numeric for bar chart"}
                    chart_data["data"] = {
                        "labels": grouped[cols[0]].astype(str).tolist(),
                        "values": grouped[cols[1]].tolist()
                    }
                else:
                    counts = df[cols[0]].value_counts().reset_index(name="count")
                    chart_data["data"] = {
                        "labels": counts[cols[0]].astype(str).tolist(),
                        "values": counts["count"].tolist()
                    }
                chart_data["metadata"]["title"] = f"{chart_data['metadata']['y_label']} by {chart_data['metadata']['x_label']}"

            elif chart_type == "pie":
                if len(cols) != 1:
                    return {"error": "Pie chart requires exactly one categorical column"}
                counts = df[cols[0]].value_counts().reset_index(name="count")
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
                sorted_df = df.sort_values(cols[0])
                chart_data["data"] = {
                    "labels": sorted_df[cols[0]].astype(str).tolist(),
                    "values": sorted_df[cols[1]].tolist()
                }
                chart_data["metadata"]["title"] = f"{chart_data['metadata']['y_label']} over {chart_data["metadata"]["x_label"]}"

            elif chart_type == "scatter":
                if len(cols) != 2:
                    return {"error": "Scatter chart requires two numeric columns"}
                if not all(np.issubdtype(df[col].dtype, np.number) for col in cols):
                    return {"error": f"Columns {cols} must be numeric for scatter chart"}
                chart_data["data"] = {
                    "data": [{"x": x, "y": y} for x, y in zip(df[cols[0]], df[cols[1]])]
                }
                chart_data["metadata"]["title"] = f"{chart_data["metadata"]["y_label"]} vs {chart_data['metadata']['x_label']}"

            else:
                return {"error": f"Unsupported chart type: {chart_type}"}
            
            charts.append(chart_data)

            return {"charts": charts}

    except Exception as e:
        return {"error": f"Failed to create chart data: {str(e)}"}