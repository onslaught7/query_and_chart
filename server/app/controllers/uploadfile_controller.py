import uuid
from fastapi import UploadFile
import pandas as pd
import io
from PyPDF2 import PdfReader
import re


# In memory store
user_sessions = {}


def parse_file(file: UploadFile):
    filename = file.filename.lower()
    print(f"✅File {file.file} received for parsing: {file.filename}")

    if filename.endswith(".csv"):
        try:
            content = file.file.read().decode("utf-8")
            df = pd.read_csv(io.StringIO(content))
            return df, df.to_string(index=False)
        except Exception as e:
            print(f"Error parsing CSV: {e}")
            raise ValueError(f"Could not parse CSV file: {e}")
        
    elif filename.endswith(".pdf"):
        try:
            reader = PdfReader(file.file)
            text = "\n".join([page.extract_text() for page in reader.pages])
            return text
        except Exception as e:
            print(f"Error parsing PDF: {e}")
            raise ValueError(f"Could not parse PDF file: {e}")
        
    elif filename.endswith(".xlsx"):
        try:
            df = pd.read_excel(file.file)
            return df, df.to_string(index=False)
        except Exception as e:
            print(f"Error parsing Excel file: {e}")
            raise ValueError(f"Could not parse Excel file: {e}")
        
    else:
        raise ValueError("Unsupported file type")


async def handle_file_upload(file: UploadFile, session_id: str = None):
    try:
        df, parsed_content = parse_file(file)
        session_data = {
            "raw_text": parsed_content,
            "dataframe": df
        }
        if session_id and session_id in user_sessions:
            user_sessions[session_id] = session_data
        else:
            session_id = str(uuid.uuid4())
            user_sessions[session_id] = session_data
        print(f"The generated session id: {session_id}") 
        print(f"The columns of the DataFrame: {df.columns.to_list()}")
        return {"session_id": session_id, "message": "File Uploaded Sucessfully"}
    except Exception as e:
        return {"error": str(e)}