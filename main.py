from fastapi import FastAPI
from role import role_router

app = FastAPI()
app.include_router(role_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Student API is working"}