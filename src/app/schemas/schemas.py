from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class CompanyBase(BaseModel):
    name: str
    industry: Optional[str] = None
    size: Optional[str] = None

class CompanyCreate(CompanyBase):
    pass

class Company(CompanyBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class JobDescriptionRequest(BaseModel):
    required_tools: List[str] = Field(..., description="List of required tools and technologies")
    company_culture: Optional[str] = Field(None, description="Optional company culture description")

class JobDescriptionSection(BaseModel):
    title: str = Field(..., description="Section title")
    content: str = Field(..., description="Section content")

class JobDescription(BaseModel):
    title: str = Field(..., description="Job title")
    overview: JobDescriptionSection = Field(..., description="Job overview section")
    responsibilities: JobDescriptionSection = Field(..., description="Job responsibilities section")
    requirements: JobDescriptionSection = Field(..., description="Job requirements section")
    qualifications: JobDescriptionSection = Field(..., description="Job qualifications section")
    benefits: JobDescriptionSection = Field(..., description="Job benefits section")

class JobPostingBase(BaseModel):
    title: str
    company_id: int

class JobPostingCreate(JobPostingBase):
    pass

class JobPosting(JobPostingBase):
    id: int
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 