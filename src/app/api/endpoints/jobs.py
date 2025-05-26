from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import openai
from ...schemas.schemas import JobDescriptionRequest, JobDescriptionResponse
from ...models.models import JobPosting
from ...database import get_db

router = APIRouter()

@router.post("/{job_id}/description", response_model=JobDescriptionResponse)
async def generate_job_description(
    job_id: int,
    request: JobDescriptionRequest,
    db: Session = Depends(get_db)
):
    # Get job posting from database
    job_posting = db.query(JobPosting).filter(JobPosting.id == job_id).first()
    if not job_posting:
        raise HTTPException(status_code=404, detail="Job posting not found")

    # Prepare the prompt for OpenAI
    prompt = f"""Generate a detailed job description for a {job_posting.title} position.
    Required tools and technologies: {', '.join(request.required_tools)}
    Company information: {job_posting.company.name if job_posting.company else 'Not specified'}
    """

    try:
        # Call OpenAI API
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional job description writer."},
                {"role": "user", "content": prompt}
            ],
            stream=True
        )

        # Collect the streamed response
        description = ""
        async for chunk in response:
            if chunk.choices[0].delta.content:
                description += chunk.choices[0].delta.content

        # Update the job posting with the generated description
        job_posting.description = description
        db.commit()

        return JobDescriptionResponse(
            job_id=job_id,
            description=description,
            generated_at=datetime.utcnow()
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating job description: {str(e)}") 