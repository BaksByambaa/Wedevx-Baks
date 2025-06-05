from fastapi import FastAPI, HTTPException, Query, Path
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Job Applications API")

# Add root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to the Job Applications API",
        "endpoints": {
            "Create application": "POST /applications",
            "List applications": "GET /applications",
            "Get application": "GET /applications/{candidate_id}",
            "Update application": "PUT /applications/{candidate_id}",
            "Patch application": "PATCH /applications/{candidate_id}",
            "Delete application": "DELETE /applications/{candidate_id}"
        }
    }

# Pydantic models
class ApplicationCreate(BaseModel):
    candidate_id: str
    name: str
    email: str
    job_id: str | None = None

class ApplicationUpdate(BaseModel):
    email: Optional[str] = None
    job_id: Optional[str] = None

# In-memory storage
applications = []     #Cache memory

@app.post("/applications")
async def create_application(application: ApplicationCreate):
    #input sanitization --> if the email fits the format or no?
    #name is at least 2 words
    #does this jobID already in the cache? if yes, update it, if no insert
    applications.append(application.dict())
    return {
        "status": "success",
        "message": f"Application submitted for {application.name}"
    }

@app.get("/applications")
async def get_applications(
    company_name: Optional[str] = Query(None, description="Filter by company name"),
    candidate_email: Optional[str] = Query(None, description="Filter by candidate email")
):
    if company_name:
        return {"message": f"Here is your application for {company_name}"}
    elif candidate_email:
        return {"message": f"Here is your application for {candidate_email}"}
    return {"message": "Here are all of your applications"}

@app.get("/applications/{candidate_id}")
async def get_application(candidate_id: str):
    for app in applications:
        if app["candidate_id"] == candidate_id:
            return {"message": f"Application found for candidate ID: {candidate_id}"}
    raise HTTPException(status_code=404, detail=f"No application found for candidate ID: {candidate_id}")

@app.put("/applications/{candidate_id}")
async def update_application(candidate_id: str, application: ApplicationUpdate):
    for app in applications:
        if app["candidate_id"] == candidate_id:
            if application.email:
                app["email"] = application.email
            if application.job_id:
                app["job_id"] = application.job_id
            return {"message": f"Application for {candidate_id} successfully updated"}
    raise HTTPException(status_code=404, detail=f"No application found for candidate ID: {candidate_id}")

@app.patch("/applications/{candidate_id}")
async def patch_application(candidate_id: str, application: ApplicationUpdate):
    for app in applications:
        if app["candidate_id"] == candidate_id:
            updated_fields = []
            if application.email:
                app["email"] = application.email
                updated_fields.append("email")
            if application.job_id:
                app["job_id"] = application.job_id
                updated_fields.append("job_id")
            return {
                "message": f"Updated fields for {candidate_id}: {', '.join(updated_fields)}"
            }
    raise HTTPException(status_code=404, detail=f"No application found for candidate ID: {candidate_id}")

@app.delete("/applications/{candidate_id}")
async def delete_application(candidate_id: str):
    for i, app in enumerate(applications):
        if app["candidate_id"] == candidate_id:
            applications.pop(i)
            return {
                "status": "success",
                "message": f"Application for {candidate_id} has been deleted"
            }
    raise HTTPException(status_code=404, detail=f"No application found for candidate ID: {candidate_id}")


