from typing import List, Literal, Optional
from pydantic import BaseModel

Priority = Literal["low", "medium", "high"]
Status = Literal["READY", "BLOCKED"]
JobStatus = Literal["PENDING", "COMPLETED", "FAILED"]

class Task(BaseModel):
    id: str
    description: str
    priority: Priority
    dependencies: List[str]
    status: Optional[Status] = None

class GenerateRequest(BaseModel):
    transcript: str
