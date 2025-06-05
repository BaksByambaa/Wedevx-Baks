# AI-Powered Job Application Bot

An automated job application bot that uses AI to generate tailored resumes and automate the job application process.

## Features

- Automated job description extraction
- AI-powered resume generation using OpenAI
- Automated form filling
- Screenshot capture of applications
- PDF resume generation

## Prerequisites

- Python 3.8+
- OpenAI API key
- Chrome browser installed

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

## Usage

Run the main script:
```bash
python job_application_bot.py
```

## Project Structure

- `job_application_bot.py`: Main application file
- `job_extractor.py`: Job description extraction module
- `job_filler.py`: Form filling automation module
- `resumes/`: Directory for generated resumes
- `screenshots/`: Directory for application screenshots

## Author

Baks Byambaa

## License

MIT
