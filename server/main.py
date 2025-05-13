from fastapi import FastAPI
from app.routes import uploadfile_routes, query_routes, generatechart_routes


app = FastAPI()


@app.get("/")
async def root():
   return {"message": "Server is up and running 🚀"}    


app.include_router(uploadfile_routes.router, prefix="/api/uploads", tags=["Uploads"])
app.include_router(query_routes.router, prefix="/api/query", tags=["Query"])
app.include_router(generatechart_routes.router, prefix="/api/charts", tags=["Charts"])