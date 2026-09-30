"""
HireMatch SDET — Database Validation Test Suite
────────────────────────────────────────────────
Validates database integrity, schema correctness, referential
constraints, and data consistency after API operations.

Demonstrates:
  • Direct SQLAlchemy ORM + raw SQL assertions
  • Schema validation (columns, types, constraints)
  • Referential integrity (FK cascade behavior)
  • Data consistency after CRUD operations
  • Index existence validation

Author: Anirudh Gupta
"""

import os
import sys
import pytest
from pathlib import Path
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker

# Add project root to path for imports
ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT / "backend"))

from app.database import Base
from app.models import User, Job, Application, SavedJob, CandidateProfile


DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{ROOT / 'hirematch.db'}")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
TestSession = sessionmaker(bind=engine)


@pytest.fixture
def db_session():
    """Provide a fresh DB session per test, rolled back on completion."""
    session = TestSession()
    yield session
    session.rollback()
    session.close()


@pytest.fixture
def inspector():
    """SQLAlchemy Inspector for schema introspection."""
    return inspect(engine)


# ═══════════════════════════════════════════════
#   SCHEMA VALIDATION TESTS
# ═══════════════════════════════════════════════

class TestSchemaValidation:
    """Validate that DB schema matches expected ORM model definitions."""

    @pytest.mark.regression
    @pytest.mark.api
    def test_all_expected_tables_exist(self, inspector):
        """Verify all ORM-declared tables are created in the database."""
        expected_tables = {"users", "candidate_profiles", "jobs", "applications", "saved_jobs"}
        actual_tables = set(inspector.get_table_names())
        missing = expected_tables - actual_tables
        assert not missing, f"Missing tables in DB: {missing}"

    @pytest.mark.regression
    def test_users_table_columns(self, inspector):
        """Validate users table has all required columns with correct types."""
        columns = {col["name"]: col for col in inspector.get_columns("users")}
        required_columns = ["id", "email", "hashed_password", "full_name", "role", "is_active", "created_at"]
        for col_name in required_columns:
            assert col_name in columns, f"Missing column 'users.{col_name}'"

    @pytest.mark.regression
    def test_jobs_table_columns(self, inspector):
        """Validate jobs table has all expected columns."""
        columns = {col["name"]: col for col in inspector.get_columns("jobs")}
        required = [
            "id", "recruiter_id", "title", "company_name", "location",
            "job_type", "experience_level", "description", "requirements",
            "skills_required", "is_active", "created_at", "updated_at"
        ]
        for col_name in required:
            assert col_name in columns, f"Missing column 'jobs.{col_name}'"

    @pytest.mark.regression
    def test_applications_table_columns(self, inspector):
        """Validate applications table schema."""
        columns = {col["name"]: col for col in inspector.get_columns("applications")}
        required = ["id", "job_id", "candidate_id", "status", "cover_letter", "applied_at"]
        for col_name in required:
            assert col_name in columns, f"Missing column 'applications.{col_name}'"

    @pytest.mark.regression
    def test_users_email_has_unique_constraint(self, inspector):
        """Email column must have a unique constraint to prevent duplicates."""
        unique_constraints = inspector.get_unique_constraints("users")
        indexes = inspector.get_indexes("users")

        # Check unique constraints or unique indexes
        email_unique = any(
            "email" in (c.get("column_names", []))
            for c in unique_constraints
        ) or any(
            "email" in idx.get("column_names", []) and idx.get("unique", False)
            for idx in indexes
        )
        assert email_unique, "users.email must have a UNIQUE constraint"

    @pytest.mark.regression
    def test_applications_unique_constraint(self, inspector):
        """Each candidate can apply to a job only once (job_id + candidate_id)."""
        unique_constraints = inspector.get_unique_constraints("applications")
        has_composite = any(
            set(c.get("column_names", [])) == {"job_id", "candidate_id"}
            for c in unique_constraints
        )
        assert has_composite, "applications must have UNIQUE(job_id, candidate_id)"

    @pytest.mark.regression
    def test_saved_jobs_unique_constraint(self, inspector):
        """Each user can save a job only once."""
        unique_constraints = inspector.get_unique_constraints("saved_jobs")
        has_composite = any(
            set(c.get("column_names", [])) == {"job_id", "user_id"}
            for c in unique_constraints
        )
        assert has_composite, "saved_jobs must have UNIQUE(job_id, user_id)"


# ═══════════════════════════════════════════════
#   FOREIGN KEY / REFERENTIAL INTEGRITY TESTS
# ═══════════════════════════════════════════════

class TestReferentialIntegrity:
    """Validate foreign key relationships between tables."""

    @pytest.mark.regression
    def test_jobs_fk_to_users(self, inspector):
        """jobs.recruiter_id must reference users.id."""
        fks = inspector.get_foreign_keys("jobs")
        recruiter_fk = [
            fk for fk in fks
            if "recruiter_id" in fk.get("constrained_columns", [])
        ]
        assert len(recruiter_fk) > 0, "jobs.recruiter_id must have FK to users"
        assert recruiter_fk[0]["referred_table"] == "users"
        assert recruiter_fk[0]["referred_columns"] == ["id"]

    @pytest.mark.regression
    def test_applications_fk_to_jobs(self, inspector):
        """applications.job_id must reference jobs.id."""
        fks = inspector.get_foreign_keys("applications")
        job_fk = [fk for fk in fks if "job_id" in fk.get("constrained_columns", [])]
        assert len(job_fk) > 0, "applications.job_id must have FK to jobs"
        assert job_fk[0]["referred_table"] == "jobs"

    @pytest.mark.regression
    def test_applications_fk_to_users(self, inspector):
        """applications.candidate_id must reference users.id."""
        fks = inspector.get_foreign_keys("applications")
        candidate_fk = [fk for fk in fks if "candidate_id" in fk.get("constrained_columns", [])]
        assert len(candidate_fk) > 0, "applications.candidate_id must have FK to users"
        assert candidate_fk[0]["referred_table"] == "users"

    @pytest.mark.regression
    def test_candidate_profiles_fk_to_users(self, inspector):
        """candidate_profiles.user_id must reference users.id."""
        fks = inspector.get_foreign_keys("candidate_profiles")
        user_fk = [fk for fk in fks if "user_id" in fk.get("constrained_columns", [])]
        assert len(user_fk) > 0, "candidate_profiles.user_id must have FK to users"
        assert user_fk[0]["referred_table"] == "users"


# ═══════════════════════════════════════════════
#   DATA CONSISTENCY & INTEGRITY TESTS
# ═══════════════════════════════════════════════

class TestDataConsistency:
    """Validate data integrity rules after seed/operations."""

    @pytest.mark.regression
    @pytest.mark.smoke
    def test_seeded_users_exist(self, db_session):
        """At least candidate and recruiter seed users must exist."""
        users = db_session.query(User).all()
        assert len(users) >= 2, f"Expected at least 2 seeded users, got {len(users)}"

    @pytest.mark.regression
    def test_all_users_have_valid_roles(self, db_session):
        """Every user.role must be either 'candidate' or 'recruiter'."""
        users = db_session.query(User).all()
        for user in users:
            assert user.role in ("candidate", "recruiter"), \
                f"User {user.email} has invalid role: {user.role}"

    @pytest.mark.regression
    def test_no_orphaned_applications(self, db_session):
        """Every application must reference a valid job and candidate."""
        result = db_session.execute(text("""
            SELECT a.id, a.job_id, a.candidate_id
            FROM applications a
            LEFT JOIN jobs j ON a.job_id = j.id
            LEFT JOIN users u ON a.candidate_id = u.id
            WHERE j.id IS NULL OR u.id IS NULL
        """)).fetchall()
        assert len(result) == 0, f"Found {len(result)} orphaned applications: {result}"

    @pytest.mark.regression
    def test_no_orphaned_saved_jobs(self, db_session):
        """Every saved_job must reference a valid job and user."""
        result = db_session.execute(text("""
            SELECT sj.id, sj.job_id, sj.user_id
            FROM saved_jobs sj
            LEFT JOIN jobs j ON sj.job_id = j.id
            LEFT JOIN users u ON sj.user_id = u.id
            WHERE j.id IS NULL OR u.id IS NULL
        """)).fetchall()
        assert len(result) == 0, f"Found {len(result)} orphaned saved jobs"

    @pytest.mark.regression
    def test_all_emails_are_unique(self, db_session):
        """No duplicate emails in the users table."""
        result = db_session.execute(text("""
            SELECT email, COUNT(*) as cnt
            FROM users
            GROUP BY email
            HAVING cnt > 1
        """)).fetchall()
        assert len(result) == 0, f"Duplicate emails found: {result}"

    @pytest.mark.regression
    def test_all_jobs_have_recruiter_role(self, db_session):
        """Every job's recruiter must have role='recruiter'."""
        result = db_session.execute(text("""
            SELECT j.id, j.title, u.email, u.role
            FROM jobs j
            JOIN users u ON j.recruiter_id = u.id
            WHERE u.role != 'recruiter'
        """)).fetchall()
        assert len(result) == 0, \
            f"Found jobs posted by non-recruiters: {[(r[0], r[2], r[3]) for r in result]}"

    @pytest.mark.regression
    def test_application_status_values(self, db_session):
        """Application status must be from the defined enum set."""
        valid_statuses = {"Applied", "Under Review", "Shortlisted", "Interview Scheduled", "Rejected", "Offered"}
        apps = db_session.query(Application).all()
        for app in apps:
            assert app.status in valid_statuses, \
                f"Application {app.id} has invalid status: {app.status}"

    @pytest.mark.regression
    def test_salary_range_consistency(self, db_session):
        """min_salary should never exceed max_salary."""
        jobs = db_session.query(Job).all()
        for job in jobs:
            assert job.min_salary <= job.max_salary, \
                f"Job '{job.title}' has invalid salary range: {job.min_salary} > {job.max_salary}"

    @pytest.mark.regression
    @pytest.mark.negative
    def test_no_null_email_users(self, db_session):
        """No user should have a NULL email (critical field)."""
        result = db_session.execute(text(
            "SELECT id FROM users WHERE email IS NULL"
        )).fetchall()
        assert len(result) == 0, f"Found users with NULL email: {result}"

    @pytest.mark.regression
    def test_created_at_not_future(self, db_session):
        """No record should have a future created_at timestamp."""
        from datetime import datetime
        users = db_session.query(User).all()
        for user in users:
            if user.created_at:
                assert user.created_at <= datetime.now(), \
                    f"User {user.email} has future created_at: {user.created_at}"
