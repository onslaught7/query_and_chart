from fastapi import APIRouter


router = APIRouter()


router.post("/query")
async def queryFile(query: str):
    pass