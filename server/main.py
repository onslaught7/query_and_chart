from fastapi import FastAPI
from app.routes import uploadfile_routes


app = FastAPI()


@app.get("/")
async def root():
   return {"message": "Server is up and running 🚀"}    


app.include_router(uploadfile_routes.router, prefix="/api/uploads", tags=["Uploads"])