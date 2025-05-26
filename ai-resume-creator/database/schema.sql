-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Companies table
CREATE TABLE companies (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name TEXT NOT NULL,
  description TEXT,
  industry TEXT,
  website TEXT,
  logo_url TEXT,
  location TEXT,
  size TEXT CHECK (size IN ('STARTUP', 'SMB', 'ENTERPRISE')),
  founded_year INTEGER,
  social_media JSONB,
  culture_values TEXT[],
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Job Postings table
CREATE TABLE job_postings (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  company_id UUID REFERENCES companies(id),
  title TEXT NOT NULL,
  description TEXT NOT NULL,
  requirements TEXT[],
  responsibilities TEXT[],
  salary_range JSONB,
  location TEXT,
  job_type TEXT CHECK (job_type IN ('FULL_TIME', 'PART_TIME', 'CONTRACT', 'REMOTE')),
  experience_level TEXT CHECK (experience_level IN ('ENTRY', 'MID', 'SENIOR', 'EXECUTIVE')),
  skills_required TEXT[],
  benefits TEXT[],
  department TEXT,
  posted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  deadline TIMESTAMP WITH TIME ZONE,
  status TEXT DEFAULT 'OPEN' CHECK (status IN ('OPEN', 'CLOSED', 'DRAFT')),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Candidates table
CREATE TABLE candidates (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID UNIQUE NOT NULL,
  personal_info JSONB NOT NULL,
  professional_summary TEXT,
  work_experience JSONB[],
  education JSONB[],
  skills JSONB[],
  certifications JSONB[],
  languages JSONB[],
  portfolio_urls TEXT[],
  preferred_job_types TEXT[],
  preferred_locations TEXT[],
  desired_salary_range JSONB,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Custom Resumes table
CREATE TABLE custom_resumes (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  candidate_id UUID REFERENCES candidates(id),
  job_id UUID REFERENCES job_postings(id),
  template_id UUID,
  content JSONB,
  ai_suggestions JSONB,
  version INTEGER DEFAULT 1,
  file_url TEXT,
  file_type TEXT CHECK (file_type IN ('PDF', 'DOCX')),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Job Applications table
CREATE TABLE job_applications (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  job_id UUID REFERENCES job_postings(id),
  candidate_id UUID REFERENCES candidates(id),
  custom_resume_id UUID REFERENCES custom_resumes(id),
  cover_letter TEXT,
  status TEXT DEFAULT 'SUBMITTED' CHECK (status IN ('DRAFT', 'SUBMITTED', 'REVIEWED', 'SHORTLISTED', 'REJECTED', 'HIRED')),
  matching_score NUMERIC,
  notes TEXT,
  interview_feedback JSONB[],
  applied_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Skills Matrix table
CREATE TABLE skills_matrix (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  skill_name TEXT UNIQUE NOT NULL,
  category TEXT,
  related_skills TEXT[],
  industry_relevance TEXT[],
  experience_levels TEXT[],
  keywords TEXT[],
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
); 