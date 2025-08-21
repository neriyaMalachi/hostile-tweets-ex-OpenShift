from fastapi import FastAPI
from fastapi.middleware.cors import (CORSMiddleware)
from app.manager import PipelineManager

app = FastAPI(title="Malicious Text Feature Engineering API", version="1.0.0")

# CORS בסיסי (לבדיקות)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/processed")
def get_processed():
    manager = PipelineManager()
    return manager.as_records()
