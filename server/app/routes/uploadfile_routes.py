from fastapi import APIRouter, UploadFile, File
from app.controllers.uploadfile_controller import handle_file_upload


router = APIRouter()


@router.post("/upload-file")
async def uploadFile(file: UploadFile):
    return await handle_file_upload(file)