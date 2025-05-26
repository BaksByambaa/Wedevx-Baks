from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import openai
import os
from .api.endpoints import jobs
from .database import engine
from .models import models

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

@app.get("/")
async def root():
    return {"message": "Welcome to the Job Description Generator API"} 