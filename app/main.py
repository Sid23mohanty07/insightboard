from fastapi import FastAPI, BackgroundTasks, HTTPException
from dotenv import load_dotenv
load_dotenv()

import uuid

from app.models import GenerateRequest
from app.jobs import process_job, transcript_hash
from app.db import jobs_collection

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="InsightBoard Dependency Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://insightboard-pr9e.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate")
def generate(req: GenerateRequest, background_tasks: BackgroundTasks):
    hash_value = transcript_hash(req.transcript)

    existing = jobs_collection.find_one({"hash": hash_value})
    if existing:
        return {
            "jobId": existing["jobId"],
            "status": existing["status"]
        }

    job_id = str(uuid.uuid4())

    jobs_collection.insert_one({
        "jobId": job_id,
        "hash": hash_value,
        "status": "PENDING"
    })

    background_tasks.add_task(
        process_job,
        job_id,
        req.transcript
    )

    return {
        "jobId": job_id,
        "status": "PENDING"
    }

@app.get("/")
def root():
    return {"status": "InsightBoard API is running"}

@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    job = jobs_collection.find_one({"jobId": job_id}, {"_id": 0})

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return job
