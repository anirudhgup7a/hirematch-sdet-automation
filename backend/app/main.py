import time
from datetime import datetime
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text
from app.config import settings
from app.database import engine, Base, SessionLocal
from app.routers import auth_router, jobs_router, applications_router, saved_jobs_router

# Initialize Database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Intelligent Job Search & Recruitment Platform REST API — SDET Test Automation Target",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Timing Middleware for SDET response time tracking
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.4f}s"
    return response

# Include API Routers
app.include_router(auth_router.router, prefix=settings.API_V1_STR)
app.include_router(jobs_router.router, prefix=settings.API_V1_STR)
app.include_router(applications_router.router, prefix=settings.API_V1_STR)
app.include_router(saved_jobs_router.router, prefix=settings.API_V1_STR)

@app.get("/health", tags=["Health"])
@app.get(f"{settings.API_V1_STR}/health", tags=["Health"])
def health_check():
    db_status = "healthy"
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    return {
        "status": "UP",
        "service": "HireMatch QA Backend",
        "version": "1.0.0",
        "database": db_status,
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Welcome to HireMatch QA — Intelligent Job Search & Recruitment Platform API",
        "docs": "/docs",
        "health": f"{settings.API_V1_STR}/health",
        "version": "1.0.0"
    }
