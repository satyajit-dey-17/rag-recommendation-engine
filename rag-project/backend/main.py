import os
import traceback
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from backend.models import WorkloadRequest
from backend.recommender import analyze_requirements

load_dotenv()

app = FastAPI(title="Multi-Cloud Recommender")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze")
def analyze(request: WorkloadRequest):
    try:
        return analyze_requirements(request)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))