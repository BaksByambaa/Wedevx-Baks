from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate
from ...database import get_db
from ...models import models
from ...schemas import schemas
import os

router = APIRouter()

@router.post("/", response_model=schemas.JobPosting)
def create_job_posting(job: schemas.JobPostingCreate, db: Session = Depends(get_db)):
    db_job = models.JobPosting(**job.dict())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

def init_chat_model():
    return ChatOpenAI(
        model_name="gpt-4",
        temperature=0.7,
        max_tokens=2000,
        model_kwargs={
            "top_p": 0.9,
            "frequency_penalty": 0.5,
            "presence_penalty": 0.5
        }
    )

def create_job_description_prompt():
    system_template = """You are an expert job description writer. Create a professional job description based on the following information:
    - Job Title: {job_title}
    - Company Name: {company_name}
    - Company Industry: {company_industry}
    - Required Tools: {required_tools}
    - Company Culture: {company_culture}

    Generate a structured job description with the following sections:
    1. Overview
    2. Responsibilities
    3. Requirements
    4. Qualifications
    5. Benefits

    Make the description professional, engaging, and tailored to the company's culture and industry."""
    
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    
    human_template = "Please generate a job description for the {job_title} position at {company_name}."
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    
    return ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

@router.post("/{job_id}/description", response_model=schemas.JobDescription)
async def generate_job_description(
    job_id: int,
    request: schemas.JobDescriptionRequest,
    db: Session = Depends(get_db)
):
    # Get job posting and company information
    job_posting = db.query(models.JobPosting).filter(models.JobPosting.id == job_id).first()
    if not job_posting:
        raise HTTPException(status_code=404, detail="Job posting not found")
    
    company = db.query(models.Company).filter(models.Company.id == job_posting.company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    # Initialize LangChain components
    chat_model = init_chat_model()
    prompt = create_job_description_prompt()
    parser = PydanticOutputParser(pydantic_object=schemas.JobDescription)

    # Prepare prompt variables
    prompt_variables = {
        "job_title": job_posting.title,
        "company_name": company.name,
        "company_industry": company.industry or "Not specified",
        "required_tools": ", ".join(request.required_tools),
        "company_culture": request.company_culture or "Not specified"
    }

    try:
        # Generate job description
        chain = prompt | chat_model | parser
        job_description = chain.invoke(prompt_variables)

        # Save to database
        job_posting.description = job_description.json()
        db.commit()
        db.refresh(job_posting)

        return job_description

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating job description: {str(e)}")

@router.get("/", response_model=List[schemas.JobPosting])
def get_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    jobs = db.query(models.JobPosting).offset(skip).limit(limit).all()
    return jobs 