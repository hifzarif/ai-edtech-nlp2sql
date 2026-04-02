from fastapi import FastAPI
from app.services.query_service import process_query
from app.analytics.stats import get_stats

app = FastAPI()

@app.post("/query")
def query_api(payload: dict):
    return process_query(payload["question"])

@app.get("/stats")
def stats():
    return get_stats()

@app.get("/")
def home():
    return {"message": "API is running 🚀"}