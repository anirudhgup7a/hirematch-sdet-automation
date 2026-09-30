export interface User {
  id: number;
  email: string;
  full_name: string;
  role: 'candidate' | 'recruiter';
  is_active: boolean;
  created_at: string;
}

export interface CandidateProfile {
  id: number;
  user_id: number;
  headline?: string;
  current_company?: string;
  experience_years: number;
  skills?: string;
  location?: string;
  resume_url?: string;
}

export interface Job {
  id: number;
  recruiter_id: number;
  title: string;
  company_name: string;
  location: string;
  job_type: string;
  experience_level: string;
  min_experience: number;
  max_experience: number;
  min_salary: number;
  max_salary: number;
  description: string;
  requirements: string;
  skills_required: string;
  is_active: boolean;
  created_at: string;
  updated_at?: string;
}

export interface Application {
  id: number;
  job_id: number;
  candidate_id: number;
  cover_letter?: string;
  resume_url?: string;
  status: 'Applied' | 'Under Review' | 'Shortlisted' | 'Interview Scheduled' | 'Rejected' | 'Offered';
  applied_at: string;
  job?: Job;
  candidate?: User;
}

export interface SavedJob {
  id: number;
  job_id: number;
  user_id: number;
  saved_at: string;
  job?: Job;
}

export interface JobListResponse {
  items: Job[];
  total: number;
  page: number;
  size: number;
  total_pages: number;
}

export interface JobFiltersState {
  keyword: string;
  location: string;
  job_type: string;
  experience_level: string;
  min_salary?: number;
  sort_by: string;
}
