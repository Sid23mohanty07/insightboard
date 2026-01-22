import hashlib
from app.llm import generate_tasks
from app.sanitize import sanitize_dependencies
from app.cycle import detect_cycles
from app.db import jobs_collection, graphs_collection

def transcript_hash(transcript: str) -> str:
    return hashlib.sha256(transcript.encode()).hexdigest()


def process_job(job_id: str, transcript: str):
    try:
        tasks = generate_tasks(transcript)
        tasks = sanitize_dependencies(tasks)

        blocked_ids = detect_cycles(tasks)
        for task in tasks:
            task["status"] = "BLOCKED" if task["id"] in blocked_ids else "READY"

        graphs_collection.insert_one({
            "jobId": job_id,
            "transcript": transcript,
            "tasks": tasks
        })

        jobs_collection.update_one(
            {"jobId": job_id},
            {"$set": {"status": "COMPLETED", "tasks": tasks}}
        )

    except Exception as e:
        jobs_collection.update_one(
            {"jobId": job_id},
            {"$set": {"status": "FAILED", "error": str(e)}}
        )
