from pydantic import BaseModel
from typing import List
from datetime import datetime

class JobDescriptionRequest(BaseModel):
    required_tools: List[str]

class JobDescriptionResponse(BaseModel):
    job_id: int
    description: str
    generated_at: datetime

class JobPostingBase(BaseModel):
    title: str
    company_id: int

class JobPostingCreate(JobPostingBase):
    pass

class JobPosting(JobPostingBase):
    id: int
    description: str | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 