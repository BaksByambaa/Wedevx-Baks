import time
from job_extractor import extract_job_fields, click_apply_button
from job_filler import fill_job_application
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
import logging
from openai import OpenAI

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create base directories if they don't exist
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESUMES_DIR = os.path.join(BASE_DIR, 'resumes')
SCREENSHOTS_DIR = os.path.join(BASE_DIR, 'screenshots')
os.makedirs(RESUMES_DIR, exist_ok=True)
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

def get_date_folder(base_dir):
    """Create and return a date-based folder path."""
    today = datetime.now().strftime("%Y-%m-%d")
    date_dir = os.path.join(base_dir, today)
    os.makedirs(date_dir, exist_ok=True)
    return date_dir

def analyze_job_description_tool(description: str) -> dict:
    """Analyzes the job description and extracts key information for application."""
    logger.info("Analyzing job description...")
    
    # Extract key information from job description
    analysis = {
        'skills': [],
        'requirements': [],
        'responsibilities': [],
        'experience_level': '',
        'job_title': ''
    }
    
    # Look for common skill keywords
    skill_keywords = {
        'programming': ['python', 'java', 'javascript', 'typescript', 'c++', 'ruby', 'go', 'rust'],
        'frameworks': ['react', 'angular', 'vue', 'django', 'flask', 'spring', 'express', 'node.js'],
        'databases': ['sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'cassandra'],
        'cloud': ['aws', 'azure', 'gcp', 'cloud', 'kubernetes', 'docker'],
        'tools': ['git', 'jenkins', 'jira', 'confluence', 'selenium', 'pytest'],
        'methodologies': ['agile', 'scrum', 'devops', 'ci/cd', 'tdd', 'bdd']
    }
    
    # Convert description to lowercase for case-insensitive matching
    desc_lower = description.lower()
    
    # Extract skills
    for category, keywords in skill_keywords.items():
        for keyword in keywords:
            if keyword in desc_lower:
                analysis['skills'].append(keyword.title())
    
    # Look for experience requirements
    experience_patterns = [
        r'(\d+)[\+]?\s*(?:years?|yrs?)\s*(?:of)?\s*experience',
        r'experience\s*(?:of)?\s*(\d+)[\+]?\s*(?:years?|yrs?)',
        r'(\d+)[\+]?\s*(?:years?|yrs?)\s*(?:in)?\s*the\s*field'
    ]
    
    for pattern in experience_patterns:
        import re
        match = re.search(pattern, desc_lower)
        if match:
            years = match.group(1)
            analysis['experience_level'] = f"{years}+ years"
            break
    
    # Extract job title (usually in the first few lines)
    first_lines = description.split('\n')[:3]
    for line in first_lines:
        if any(title in line.lower() for title in ['engineer', 'developer', 'architect', 'lead', 'manager']):
            analysis['job_title'] = line.strip()
            break
    
    # Extract requirements and responsibilities
    lines = description.split('\n')
    current_section = None
    
    for line in lines:
        line_lower = line.lower()
        if 'requirements' in line_lower or 'qualifications' in line_lower:
            current_section = 'requirements'
        elif 'responsibilities' in line_lower or 'duties' in line_lower:
            current_section = 'responsibilities'
        elif current_section and line.strip():
            if current_section == 'requirements':
                analysis['requirements'].append(line.strip())
            elif current_section == 'responsibilities':
                analysis['responsibilities'].append(line.strip())
    
    logger.info(f"Analysis completed. Found {len(analysis['skills'])} skills, {len(analysis['requirements'])} requirements.")
    return analysis

def generate_resume_content_tool(job_description: str) -> str:
    """Generate tailored resume content based on job description using OpenAI."""
    logger.info("Generating tailored resume content using OpenAI...")
    
    try:
        # Initialize OpenAI client
        client = OpenAI()
        
        # Create a prompt for OpenAI
        prompt = f"""Based on the following job description, generate a professional resume that highlights relevant skills and experience. 
        Format the resume in a clear, professional structure with sections for Professional Summary, Technical Skills, Work Experience, Education, Projects, and Certifications.
        Make sure to emphasize skills and experiences that match the job requirements.
        
        Job Description:
        {job_description}
        
        Generate a well-structured resume that would make the candidate stand out for this position."""
        
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",  # Using the latest GPT-4 model
            messages=[
                {"role": "system", "content": "You are a professional resume writer with expertise in creating tailored resumes for technical positions."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        # Extract the generated resume content
        resume_content = response.choices[0].message.content
        
        logger.info("Resume content generated successfully using OpenAI")
        return resume_content
        
    except Exception as e:
        logger.error(f"Error generating resume with OpenAI: {e}")
        # Fallback to a basic template if OpenAI fails
        return """
        Professional Summary:
        Experienced software engineer with expertise in Python, Selenium, and Web Automation. 
        Proven track record in developing and maintaining robust applications.
        
        Technical Skills:
        Python, Selenium, Web Automation, API Development, Test Automation, Problem Solving, Team Collaboration
        
        Work Experience:
        Senior Software Engineer
        Tech Company | 2020 - Present
        • Led development of automated testing framework
        • Implemented CI/CD pipelines
        • Mentored junior developers
        
        Education:
        Bachelor of Science in Computer Science
        University Name | 2016 - 2020
        
        Projects:
        • Automated Testing Framework
        • Web Application Development
        • API Integration Projects
        
        Certifications:
        • AWS Certified Developer
        • Python Programming Certification
        """

def create_resume_pdf_tool(content: str) -> str | None:
    """Creates a PDF resume from the generated content."""
    logger.info("Placeholder Tool: Creating PDF resume...")
    
    # Create a unique filename with timestamp
    timestamp = datetime.now().strftime("%H%M%S")
    date_dir = get_date_folder(RESUMES_DIR)
    pdf_path = os.path.join(date_dir, f"resume_{timestamp}.pdf")
    
    # Create PDF (using reportlab - make sure it's installed)
    try:
        doc = SimpleDocTemplate(pdf_path, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Add content to PDF
        # Basic splitting by lines/sections - a real implementation might need more robust parsing
        for section in content.split('\n\n'):
            if section.strip():
                # Use Paragraph for potentially multi-line text with styles
                p = Paragraph(section, styles["Normal"])
                story.append(p)
                story.append(Spacer(1, 12)) # Add some space between sections
        
        doc.build(story)
        logger.info(f"PDF resume created at: {pdf_path}")
        return pdf_path
    except ImportError:
        logger.error("ReportLab not installed. Cannot create PDF. Run: pip install reportlab")
        return None
    except Exception as e:
        logger.error(f"Error building PDF {pdf_path}: {e}")
        return None # Indicate failure

class ResumeGeneratorAgent:
    """Agent that coordinates the resume generation process."""
    def __init__(self):
        pass
    
    def generate_resume(self, job_description: str) -> str | None:
        """Generates a tailored resume based on the job description."""
        logger.info("Starting resume generation process...")
        
        try:
            # Step 1: Analyze job description
            analysis = analyze_job_description_tool(job_description)
            
            # Step 2: Generate tailored resume content
            resume_content = generate_resume_content_tool(job_description)
            
            # Step 3: Create PDF resume
            pdf_path = create_resume_pdf_tool(resume_content)
            
            if pdf_path:
                logger.info(f"Resume generated successfully at: {pdf_path}")
                return pdf_path
            else:
                logger.warning("Resume generation process failed or returned no path. Continuing without resume upload.")
                return None
        except Exception as e:
            logger.error(f"Error during resume generation process: {e}")
            return None

# Initialize the resume generator agent (placeholder)
resume_agent = ResumeGeneratorAgent()

def apply_for_job(url):
    """
    Main function to extract job description, generate tailored resume (simulated),
    and fill out the application form.
    """
    driver = None
    try:
        logger.info("Starting job application process...")
        
        # Step 1: Extract job description
        logger.info("Extracting job description...")
        driver, job_description = extract_job_fields(url)
        logger.info("Successfully extracted job description.")
        
        # Step 2: Generate tailored resume (Simulated Langchain step)
        logger.info("Generating tailored resume...")
        resume_path = resume_agent.generate_resume(job_description)
        if resume_path:
            logger.info(f"Resume generated successfully at: {resume_path}")
        else:
            logger.warning("Resume generation failed or returned no path. Continuing without resume upload.")
            resume_path = None
        
        # Step 3: Click Apply to reveal the form
        logger.info("Clicking Apply button...")
        click_apply_button(driver)

        # Step 4: Fill out the application form
        logger.info("Filling out application form...")
        fill_job_application(driver, resume_path=resume_path)
        
        logger.info("Application process completed.")
        
        # Capture screenshot before closing
        timestamp = datetime.now().strftime("%H%M%S")
        date_dir = get_date_folder(SCREENSHOTS_DIR)
        screenshot_path = os.path.join(date_dir, f"application_{timestamp}.png")
        logger.info(f"Capturing screenshot to: {screenshot_path}")
        try:
            driver.save_screenshot(screenshot_path)
            logger.info("Screenshot captured successfully")
        except Exception as e:
            logger.warning(f"Could not capture screenshot: {e}")
        
    except Exception as e:
        logger.error(f"Error during job application: {e}")
    finally:
        # Ensure the driver is quit even if errors occur
        if driver:
            logger.info("Quitting driver...")
            driver.quit()
            logger.info("Browser closed.")
        else:
             logger.info("Driver was not initialized or already quit.")

if __name__ == "__main__":
    # Use provided URL or default to Ashby careers page
    url = sys.argv[1] if len(sys.argv) > 1 else "https://www.ashbyhq.com/careers"
    apply_for_job(url) 