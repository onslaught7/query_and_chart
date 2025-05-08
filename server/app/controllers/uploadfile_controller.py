import uuid
from fastapi import UploadFile
import pandas as pd
import io
from PyPDF2 import PdfReader


# In memory store
user_sessions = {}


def parse_file(file: UploadFile):
    filename = file.filename.lower()
    print(f"✅File {file.file} received at the parse_file function in uploadfile_controller.py: {file.filename}")
    if filename.endswith(".csv"):
        content = file.file.read().decode("utf-8")
        df = pd.read_csv(io.StringIO(content))
        return df.to_string(index=False)
    elif filename.endswith(".pdf"):
        reader = PdfReader(file.file)
        text = "\n".join([page.extract_text() for page in reader.pages])
        return text
    else:
        raise ValueError("Unsupported file type")


async def handle_file_upload(file: UploadFile, session_id: str = None):
    try:
        parsed_content = parse_file(file)
        if session_id and session_id in user_sessions:
            user_sessions[session_id] = parsed_content
        else:
            session_id = str(uuid.uuid4())
            user_sessions[session_id] = parsed_content
        print(f"The generated session id: {session_id}") 
        return {"session_id": session_id, "message": "File Uploaded Sucessfully"}
    except Exception as e:
        return {"error": str(e)}