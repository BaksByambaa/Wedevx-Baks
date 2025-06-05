from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import openai
import os
import sys
from pathlib import Path

# Add the project root directory to Python path
project_root = str(Path(__file__).parent.parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from src.app.api.endpoints import jobs, companies
from src.app.database import engine
from src.app.models import models

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="Job Description Generator API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure OpenAI with environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Include routers
app.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
app.include_router(companies.router, prefix="/companies", tags=["companies"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Job Description Generator API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 