export type CompanySize = 'STARTUP' | 'SMB' | 'ENTERPRISE';
export type JobType = 'FULL_TIME' | 'PART_TIME' | 'CONTRACT' | 'REMOTE';
export type ExperienceLevel = 'ENTRY' | 'MID' | 'SENIOR' | 'EXECUTIVE';
export type JobStatus = 'OPEN' | 'CLOSED' | 'DRAFT';
export type ApplicationStatus = 'DRAFT' | 'SUBMITTED' | 'REVIEWED' | 'SHORTLISTED' | 'REJECTED' | 'HIRED';
export type FileType = 'PDF' | 'DOCX';

export interface Company {
  id: string;
  name: string;
  description?: string;
  industry?: string;
  website?: string;
  logo_url?: string;
  location?: string;
  size: CompanySize;
  founded_year?: number;
  social_media?: {
    linkedin?: string;
    twitter?: string;
  };
  culture_values?: string[];
  created_at: string;
  updated_at: string;
}

export interface JobPosting {
  id: string;
  company_id: string;
  title: string;
  description: string;
  requirements?: string[];
  responsibilities?: string[];
  salary_range?: {
    min: number;
    max: number;
  };
  location?: string;
  job_type: JobType;
  experience_level: ExperienceLevel;
  skills_required?: string[];
  benefits?: string[];
  department?: string;
  posted_at: string;
  deadline?: string;
  status: JobStatus;
  created_at: string;
  updated_at: string;
}

export interface Candidate {
  id: string;
  user_id: string;
  personal_info: {
    first_name: string;
    last_name: string;
    email: string;
    phone?: string;
    location?: string;
  };
  professional_summary?: string;
  work_experience?: {
    title: string;
    company: string;
    location?: string;
    start_date: string;
    end_date?: string;
    description?: string;
    achievements?: string[];
  }[];
  education?: {
    degree: string;
    institution: string;
    field: string;
    graduation_date: string;
    gpa?: number;
  }[];
  skills?: {
    name: string;
    level: string;
  }[];
  certifications?: {
    name: string;
    issuer: string;
    date: string;
    expiry?: string;
  }[];
  languages?: {
    name: string;
    proficiency: string;
  }[];
  portfolio_urls?: string[];
  preferred_job_types?: JobType[];
  preferred_locations?: string[];
  desired_salary_range?: {
    min: number;
    max: number;
  };
  created_at: string;
  updated_at: string;
}

export interface CustomResume {
  id: string;
  candidate_id: string;
  job_id: string;
  template_id?: string;
  content: {
    summary: string;
    highlighted_skills: string[];
    selected_experience: string[];
    selected_education: string[];
    selected_certifications: string[];
  };
  ai_suggestions?: {
    keywords: string[];
    improvement_points: string[];
    match_score: number;
  };
  version: number;
  file_url?: string;
  file_type: FileType;
  created_at: string;
  updated_at: string;
}

export interface JobApplication {
  id: string;
  job_id: string;
  candidate_id: string;
  custom_resume_id: string;
  cover_letter?: string;
  status: ApplicationStatus;
  matching_score?: number;
  notes?: string;
  interview_feedback?: {
    stage: string;
    feedback: string;
    interviewer: string;
    date: string;
  }[];
  applied_at: string;
  updated_at: string;
}

export interface SkillsMatrix {
  id: string;
  skill_name: string;
  category?: string;
  related_skills?: string[];
  industry_relevance?: string[];
  experience_levels?: ExperienceLevel[];
  keywords?: string[];
  created_at: string;
  updated_at: string;
} 