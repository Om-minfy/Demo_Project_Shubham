from fastapi import FastAPI
from app.routers import users, tasks

app = FastAPI(title="FastAPI ", version="1.0.0")

app.include_router(users.router)
app.include_router(tasks.router)

@app.get("/")
def root():
    return {"message": "FastAPI running"}