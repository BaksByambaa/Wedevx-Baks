# AI Resume Creator and Job Application System

## Project Overview
This system helps match job seekers with opportunities by managing job postings, candidate profiles, and customized resumes using AI assistance.

## Database Schema

### Main Entities
1. **Companies**
   - Stores company information
   - Includes size, industry, and culture data

2. **Job Postings**
   - Contains job descriptions and requirements
   - Links to company information
   - Tracks posting status and deadlines

3. **Candidates**
   - Stores candidate profiles
   - Includes work history, education, and skills
   - Manages job preferences

4. **Custom Resumes**
   - AI-optimized resumes for specific jobs
   - Tracks versions and improvements
   - Stores generated documents

5. **Job Applications**
   - Links candidates to job postings
   - Tracks application status
   - Stores interview feedback

6. **Skills Matrix**
   - Maintains skill relationships
   - Helps with job matching
   - Supports skill recommendations

## Setup Instructions

### Prerequisites
- PostgreSQL 12+
- Supabase Account
- Node.js 14+

### Database Setup
1. Create a new Supabase project
2. Run the schema.sql file in SQL Editor
3. Run the seed.sql file for sample data

### Environment Variables
```env
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_key
```

## Entity Relationships
- Company ←1:N→ JobPosting
- JobPosting ←1:N→ JobApplication
- Candidate ←1:N→ JobApplication
- Candidate ←1:N→ CustomResume
- JobPosting ←1:N→ CustomResume

## Features
- AI-powered resume customization
- Automated job matching
- Application tracking
- Skill gap analysis
- Interview feedback management

## Development
- Clone the repository
- Install dependencies
- Set up environment variables
- Run database migrations

## Contributing
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License
MIT License 