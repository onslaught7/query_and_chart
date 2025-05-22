import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

def preprocess_dataframe(session_id: str, required_columns: list = None):
    """
    Preprocess the DataFrame for visualization and calculations.
    
    Args:
        session_id (str): Session ID to retrieve the DataFrame.
        required_columns (list): List of columns to preprocess (optional).
    
    Returns:
        pd.DataFrame: Cleaned DataFrame.
        dict: Log of preprocessing actions.
    """
    if session_id not in user_sessions:
        return None, {"error": "Invalid or expired session"}
    
    df = user_sessions[session_id]["dataframe"].copy()
    if df is None:
        return None, {"error": "No DataFrame available"}
    
    log = []
    
    # Step 1: Subset to required columns (if provided)
    if required_columns:
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            return None, {"error": f"Columns {missing_cols} not found in DataFrame"}
        df = df[required_columns]
        log.append(f"Subset to columns: {required_columns}")
    
    # Step 2: Handle missing values
    missing_counts = df.isnull().sum()
    for col in df.columns:
        if missing_counts[col] > 0:
            if df[col].dtype in [np.float64, np.int64]:
                median = df[col].median()
                df[col].fillna(median, inplace=True)
                log.append(f"Imputed {missing_counts[col]} missing values in {col} with median {median}")
            else:
                mode = df[col].mode()[0] if not df[col].mode().empty else "Unknown"
                df[col].fillna(mode, inplace=True)
                log.append(f"Imputed {missing_counts[col]} missing values in {col} with mode {mode}")
    
    # Step 3: Remove duplicates
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        df.drop_duplicates(inplace=True)
        log.append(f"Removed {duplicates} duplicate rows")
    
    # Step 4: Correct data types
    for col in df.columns:
        if df[col].dtype == "object":
            try:
                df[col] = pd.to_numeric(df[col], errors="coerce")
                if df[col].notnull().any():
                    log.append(f"Converted {col} to numeric")
            except:
                pass
        if df[col].dtype == "object":
            try:
                df[col] = pd.to_datetime(df[col], errors="coerce")
                if df[col].notnull().any():
                    log.append(f"Converted {col} to datetime")
            except:
                pass
        if df[col].dtype == "object" and df[col].nunique() < 10:
            df[col] = df[col].astype("category")
            log.append(f"Converted {col} to categorical")
    
    # Step 5: Normalize text data
    for col in df.select_dtypes(include=["object", "category"]).columns:
        df[col] = df[col].str.lower().str.strip()
        log.append(f"Normalized text in {col}")
    
    # Step 6: Handle outliers (for numeric columns)
    for col in df.select_dtypes(include=[np.number]).columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers = ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()
        if outliers > 0:
            df[col] = df[col].clip(lower=lower_bound, upper=upper_bound)
            log.append(f"Capped {outliers} outliers in {col}")
    
    # Step 7: Standardize numeric data
    scaler = StandardScaler()
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
        log.append(f"Standardized numeric columns: {list(numeric_cols)}")
    
    # Step 8: Encode categorical variables (if needed for calculations)
    for col in df.select_dtypes(include=["category"]).columns:
        if df[col].nunique() <= 10:
            df = pd.get_dummies(df, columns=[col], prefix=col)
            log.append(f"One-hot encoded {col}")
    
    # Step 9: Validate data integrity
    for col in df.select_dtypes(include=[np.number]).columns:
        if (df[col] < 0).any() and "age" in col.lower():
            df[col] = df[col].clip(lower=0)
            log.append(f"Clipped negative values in {col}")
    
    # Update session data
    user_sessions[session_id]["dataframe"] = df
    return df, {"log": log}