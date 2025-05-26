# AI-Powered Job Description Generator

This project implements an AI-powered job description generator using FastAPI and OpenAI's GPT model. It allows users to generate detailed job descriptions based on company information and required tools.

## Features

- Generate job descriptions using OpenAI's GPT model
- Stream responses for real-time generation
- Store job descriptions in a SQLite database
- RESTful API endpoints for job management

## Prerequisites

- Python 3.8+
- OpenAI API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/BaksByambaa/Wedevx-Baks.git
cd Wedevx-Baks
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the project root and add:
```
OPENAI_API_KEY=your_openai_api_key
```

## Running the Application

Start the FastAPI server:
```bash
uvicorn src.app.main:app --reload
```

The API will be available at:
- Main URL: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## API Endpoints

### Generate Job Description
```
POST /jobs/{job_id}/description
```

Request body:
```json
{
    "required_tools": ["Python", "TensorFlow", "PyTorch", "AWS"]
}
```

## Project Structure

```
src/
└── app/
    ├── api/
    │   └── endpoints/
    │       └── jobs.py
    ├── models/
    │   └── models.py
    ├── schemas/
    │   └── schemas.py
    ├── database.py
    └── main.py
```

## Author

Baks Byambaa 