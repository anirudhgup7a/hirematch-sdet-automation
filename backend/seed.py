"""Database Seeder for HireMatch QA Platform.
Populates realistic users, recruiters, jobs, applications, and saved jobs.
"""
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from app.database import SessionLocal, Base, engine
from app.models import User, CandidateProfile, Job, Application, SavedJob
from app.auth import get_password_hash

def seed_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Clear existing data to allow fresh re-seeding
    db.query(SavedJob).delete()
    db.query(Application).delete()
    db.query(Job).delete()
    db.query(CandidateProfile).delete()
    db.query(User).delete()
    db.commit()

    print("[INFO] Seeding Users & Recruiters...")
    default_pwd = get_password_hash("Password123!")

    # 1. Recruiters
    recruiter_1 = User(
        email="recruiter1@hirematch.com",
        hashed_password=default_pwd,
        full_name="Priya Sharma",
        role="recruiter",
        is_active=True
    )
    recruiter_2 = User(
        email="recruiter2@hirematch.com",
        hashed_password=default_pwd,
        full_name="Rajesh Verma",
        role="recruiter",
        is_active=True
    )
    db.add_all([recruiter_1, recruiter_2])
    db.commit()
    db.refresh(recruiter_1)
    db.refresh(recruiter_2)

    # 2. Candidates
    candidate_1 = User(
        email="candidate1@hirematch.com",
        hashed_password=default_pwd,
        full_name="Aarav Patel",
        role="candidate",
        is_active=True
    )
    candidate_2 = User(
        email="candidate2@hirematch.com",
        hashed_password=default_pwd,
        full_name="Sneha Reddy",
        role="candidate",
        is_active=True
    )
    candidate_3 = User(
        email="anirudh@hirematch.com",
        hashed_password=default_pwd,
        full_name="Anirudh Gupta",
        role="candidate",
        is_active=True
    )
    db.add_all([candidate_1, candidate_2, candidate_3])
    db.commit()
    db.refresh(candidate_1)
    db.refresh(candidate_2)
    db.refresh(candidate_3)

    # Candidate Profiles
    profile_1 = CandidateProfile(
        user_id=candidate_1.id,
        headline="Full Stack Software Engineer | React & Python",
        current_company="TechStack Solutions",
        experience_years=3.0,
        skills="React, TypeScript, Python, FastAPI, Docker, PostgreSQL",
        location="Bengaluru, Karnataka",
        resume_url="https://hirematch.storage/resumes/aarav_patel.pdf"
    )
    profile_2 = CandidateProfile(
        user_id=candidate_2.id,
        headline="SDET / QA Automation Engineer | Playwright, Pytest, CI/CD",
        current_company="QualityMinds",
        experience_years=2.5,
        skills="Playwright, Pytest, Python, Selenium, Postman, Jenkins",
        location="Hyderabad, Telangana",
        resume_url="https://hirematch.storage/resumes/sneha_reddy.pdf"
    )
    profile_3 = CandidateProfile(
        user_id=candidate_3.id,
        headline="Aspiring SDET & Backend Developer | B.Tech CSE",
        current_company="Academic Project Contributor",
        experience_years=1.0,
        skills="Playwright, Python, FastAPI, Pytest, REST APIs, Docker, Git",
        location="Noida, Uttar Pradesh",
        resume_url="https://hirematch.storage/resumes/anirudh_gupta.pdf"
    )
    db.add_all([profile_1, profile_2, profile_3])
    db.commit()

    print("[INFO] Seeding Realistic Job Postings...")
    jobs = [
        Job(
            recruiter_id=recruiter_1.id,
            title="Software Development Engineer in Test (SDET)",
            company_name="ZetaCloud Technologies",
            location="Bengaluru",
            job_type="Full-time",
            experience_level="Mid-level (3-5 yrs)",
            min_experience=2,
            max_experience=5,
            min_salary=1200000,
            max_salary=2200000,
            description="We are seeking an SDET to design and execute robust test automation frameworks for our distributed cloud platform. You will lead UI automation with Playwright and backend testing with Pytest.",
            requirements="2+ years experience in automated testing with Python or Java. Proven expertise in Playwright/Selenium, REST API testing, and CI/CD pipelines.",
            skills_required="Playwright, Python, Pytest, REST API, Docker, CI/CD"
        ),
        Job(
            recruiter_id=recruiter_1.id,
            title="Senior QA Automation Architect",
            company_name="ZetaCloud Technologies",
            location="Bengaluru",
            job_type="Hybrid",
            experience_level="Lead (8+ yrs)",
            min_experience=6,
            max_experience=10,
            min_salary=2600000,
            max_salary=4500000,
            description="Lead the quality engineering roadmap across multiple microservices. Architect scalable test execution platforms, performance test benches, and quality governance metrics.",
            requirements="8+ years SDET experience. Strong system architecture knowledge, performance testing (Locust/k6), and cross-browser automation at scale.",
            skills_required="Playwright, Python, Kubernetes, Locust, Architecture, Allure"
        ),
        Job(
            recruiter_id=recruiter_2.id,
            title="QA Engineer (Playwright & API Testing)",
            company_name="BharatFin Digital",
            location="Gurgaon",
            job_type="Full-time",
            experience_level="Mid-level (3-5 yrs)",
            min_experience=1,
            max_experience=4,
            min_salary=900000,
            max_salary=1600000,
            description="Join India's fastest-growing fintech team to automate end-to-end user journeys for high-volume financial payments and account services.",
            requirements="Experience in test automation frameworks, API validation (HTTP status codes, schemas, idempotency), and database verification.",
            skills_required="Playwright, TypeScript, Python, Pytest, SQL, Postman"
        ),
        Job(
            recruiter_id=recruiter_2.id,
            title="Junior QA Analyst / Automation Fresher",
            company_name="BharatFin Digital",
            location="Gurgaon",
            job_type="Full-time",
            experience_level="Entry-level (0-2 yrs)",
            min_experience=0,
            max_experience=2,
            min_salary=600000,
            max_salary=950000,
            description="Entry-level opportunity for enthusiastic CS graduates with strong testing fundamentals, scripting skills, and passion for software quality.",
            requirements="B.Tech/B.E in Computer Science or equivalent. Good understanding of STLC, test cases, bug tracking, and basic Python/JavaScript.",
            skills_required="Python, Manual Testing, Test Cases, Git, Basic SQL"
        ),
        Job(
            recruiter_id=recruiter_1.id,
            title="Senior Backend Engineer (FastAPI & Microservices)",
            company_name="NexaPay Systems",
            location="Noida",
            job_type="Full-time",
            experience_level="Senior (5-8 yrs)",
            min_experience=4,
            max_experience=8,
            min_salary=1800000,
            max_salary=3200000,
            description="Build ultra-low latency transaction processing APIs using FastAPI, PostgreSQL, and Redis. High availability systems handling millions of daily events.",
            requirements="Expert in Python, FastAPI/Django, relational databases, caching, and distributed system design.",
            skills_required="Python, FastAPI, PostgreSQL, Redis, Docker, System Design"
        ),
        Job(
            recruiter_id=recruiter_1.id,
            title="Frontend Engineer (React, TypeScript & Tailwind)",
            company_name="SwasthyaTech Labs",
            location="Bengaluru",
            job_type="Remote",
            experience_level="Mid-level (3-5 yrs)",
            min_experience=2,
            max_experience=5,
            min_salary=1100000,
            max_salary=1900000,
            description="Build interactive, accessible, and high-performance patient monitoring dashboards and healthcare professional portals.",
            requirements="Solid experience in React 18, TypeScript, modern CSS, state management, and web accessibility standards.",
            skills_required="React, TypeScript, TailwindCSS, Vite, REST APIs"
        ),
        Job(
            recruiter_id=recruiter_2.id,
            title="Full Stack Software Engineer",
            company_name="Edvance Learning",
            location="Pune",
            job_type="Hybrid",
            experience_level="Mid-level (3-5 yrs)",
            min_experience=3,
            max_experience=6,
            min_salary=1400000,
            max_salary=2400000,
            description="Work across our modern ed-tech stack spanning interactive video lessons, automated grading engines, and real-time student analytics.",
            requirements="Full stack proficiency with React/Vue and Python/Node. Experience writing unit, integration, and e2e tests.",
            skills_required="React, Python, Node.js, PostgreSQL, Docker, Pytest"
        ),
        Job(
            recruiter_id=recruiter_2.id,
            title="DevOps & Cloud Reliability Engineer",
            company_name="InnoGrid Cloud",
            location="Remote",
            job_type="Remote",
            experience_level="Senior (5-8 yrs)",
            min_experience=3,
            max_experience=7,
            min_salary=1600000,
            max_salary=2800000,
            description="Scale multi-region cloud infrastructure on AWS and GCP. Manage Kubernetes clusters, CI/CD pipelines, and observability stacks.",
            requirements="Expertise with Terraform, Kubernetes, Helm, GitHub Actions, and Prometheus/Grafana monitoring.",
            skills_required="Docker, Kubernetes, Terraform, AWS, GitHub Actions, Linux"
        ),
        Job(
            recruiter_id=recruiter_1.id,
            title="Data Platform Engineer",
            company_name="QuantMetrics Analytics",
            location="Hyderabad",
            job_type="Full-time",
            experience_level="Mid-level (3-5 yrs)",
            min_experience=3,
            max_experience=6,
            min_salary=1500000,
            max_salary=2600000,
            description="Design and optimize massive-scale batch and streaming data pipelines feeding business intelligence dashboards.",
            requirements="Proficiency in PySpark, SQL, BigQuery, Airflow, and data warehouse modeling principles.",
            skills_required="Python, SQL, PySpark, Airflow, BigQuery, ETL"
        ),
        Job(
            recruiter_id=recruiter_2.id,
            title="Application Security Engineer (AppSec)",
            company_name="CyberKavach Labs",
            location="Noida",
            job_type="Hybrid",
            experience_level="Mid-level (3-5 yrs)",
            min_experience=3,
            max_experience=6,
            min_salary=1700000,
            max_salary=2900000,
            description="Perform security code reviews, automated DAST/SAST integration into CI/CD, and vulnerability assessments on cloud applications.",
            requirements="Strong understanding of OWASP Top 10, penetration testing, authentication flows (OAuth/JWT), and security test automation.",
            skills_required="AppSec, OWASP, Python, Security Testing, BurpSuite, CI/CD"
        ),
        Job(
            recruiter_id=recruiter_1.id,
            title="Mobile Application Engineer (Flutter & iOS)",
            company_name="RetailPulse Mobility",
            location="Mumbai",
            job_type="Full-time",
            experience_level="Mid-level (3-5 yrs)",
            min_experience=2,
            max_experience=5,
            min_salary=1200000,
            max_salary=2100000,
            description="Build consumer-facing shopping and loyalty applications for millions of retail shoppers across India.",
            requirements="Expertise in Flutter/Dart, state management (Bloc/Riverpod), clean architecture, and automated UI testing.",
            skills_required="Flutter, Dart, Mobile Testing, iOS, Android, REST"
        ),
        Job(
            recruiter_id=recruiter_2.id,
            title="Associate Software Engineer (Graduate Program)",
            company_name="TechCorp India",
            location="Hyderabad",
            job_type="Full-time",
            experience_level="Entry-level (0-2 yrs)",
            min_experience=0,
            max_experience=1,
            min_salary=650000,
            max_salary=1000000,
            description="Structured graduate training program for top engineering talent. Rotate across core platform engineering, product development, and QA teams.",
            requirements="Strong computer science fundamentals, data structures, algorithms, and passion for engineering excellence.",
            skills_required="Python, C++, Java, Problem Solving, Data Structures"
        )
    ]
    db.add_all(jobs)
    db.commit()
    for j in jobs:
        db.refresh(j)

    print("[INFO] Seeding Applications and Saved Jobs...")
    # Seed applications
    app1 = Application(
        job_id=jobs[0].id,  # SDET at ZetaCloud
        candidate_id=candidate_2.id,  # Sneha Reddy
        cover_letter="I have extensive experience with Playwright and Pytest frameworks. I would love to contribute to ZetaCloud.",
        resume_url="https://hirematch.storage/resumes/sneha_reddy.pdf",
        status="Shortlisted"
    )
    app2 = Application(
        job_id=jobs[2].id,  # QA Engineer at BharatFin
        candidate_id=candidate_3.id,  # Anirudh Gupta
        cover_letter="I am very excited about fintech automation and building reliable test benches for high-volume transactions.",
        resume_url="https://hirematch.storage/resumes/anirudh_gupta.pdf",
        status="Under Review"
    )
    app3 = Application(
        job_id=jobs[4].id,  # Senior Backend at NexaPay
        candidate_id=candidate_1.id,  # Aarav Patel
        cover_letter="Passionate about Python microservice architectures and high performance APIs.",
        resume_url="https://hirematch.storage/resumes/aarav_patel.pdf",
        status="Interview Scheduled"
    )
    db.add_all([app1, app2, app3])

    # Seed saved jobs
    saved1 = SavedJob(job_id=jobs[0].id, user_id=candidate_3.id)
    saved2 = SavedJob(job_id=jobs[1].id, user_id=candidate_3.id)
    saved3 = SavedJob(job_id=jobs[2].id, user_id=candidate_1.id)
    db.add_all([saved1, saved2, saved3])

    db.commit()
    db.close()
    print("[SUCCESS] Database successfully seeded with 5 users, 12 jobs, 3 applications, and 3 saved jobs!")

if __name__ == "__main__":
    seed_database()
