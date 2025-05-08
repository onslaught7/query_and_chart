# Routes to controller for managing the uploaded files 
from fastapi import APIRouter


router = APIRouter()


@router.post("/upload-file")
async def uploadFile():
    pass