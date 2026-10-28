
from pathlib import Path

from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app import models
from app.database import engine, SessionLocal
from app.routers import (
    companies,
    jobs,
    interviews,
    auth,
    contacts,
    applications,
)


# Middleware to protect all frontend pages
class FrontendLoginMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # Allow the login page without authentication
        if path == "/frontend/login":
            return await call_next(request)

        # Protect every other frontend page
        if path.startswith("/frontend"):
            if request.session.get("user_id") is None:
                return RedirectResponse(
                    url="/frontend/login",
                    status_code=303,
                )

        return await call_next(request)


# Create FastAPI application
app = FastAPI(
    title="CareerTrack API",
    description="Job Application & Recruiter Follow-up Platform",
    version="1.0.0",
)

# IMPORTANT: Register login middleware first
app.add_middleware(FrontendLoginMiddleware)

# Register session middleware second so it wraps the login middleware
app.add_middleware(
    SessionMiddleware,
    secret_key=auth.SECRET_KEY,
)


# Register existing API routers
app.include_router(companies.router)
app.include_router(jobs.router)
app.include_router(interviews.router)
app.include_router(auth.router)
app.include_router(contacts.router)
app.include_router(applications.router)


# Create database tables if needed
models.Base.metadata.create_all(bind=engine)


# Configure templates and static files
BASE_DIR = Path(__file__).resolve().parent

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)

app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "static")),
    name="static",
)


# Database session for frontend pages
def get_dashboard_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Frontend dashboard
@app.get("/frontend", response_class=HTMLResponse)
async def frontend_home(
    request: Request,
    db: Session = Depends(get_dashboard_db),
):
    application_records = (
        db.query(models.Applications)
        .order_by(models.Applications.id.desc())
        .all()
    )

    company_records = (
        db.query(models.Companies)
        .order_by(models.Companies.id.desc())
        .all()
    )

    total_applications = (
        db.query(models.Applications).count()
    )

    interview_count = (
        db.query(models.Applications)
        .filter(models.Applications.status == "Interview")
        .count()
    )

    selected_count = (
        db.query(models.Applications)
        .filter(models.Applications.status == "Selected")
        .count()
    )

    rejected_count = (
        db.query(models.Applications)
        .filter(models.Applications.status == "Rejected")
        .count()
    )

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "page_title": "CareerTracker",
            "applications": application_records,
            "total_applications": total_applications,
            "interview_count": interview_count,
            "selected_count": selected_count,
            "rejected_count": rejected_count,
            "companies": company_records,
        },
    )


# Companies page
@app.get("/frontend/companies", response_class=HTMLResponse)
async def companies_page(
    request: Request,
    db: Session = Depends(get_dashboard_db),
):
    company_records = (
        db.query(models.Companies)
        .order_by(models.Companies.id.desc())
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="companies.html",
        context={
            "page_title": "Companies",
            "companies": company_records,
        },
    )


# Jobs page
@app.get("/frontend/jobs", response_class=HTMLResponse)
async def jobs_page(
    request: Request,
    db: Session = Depends(get_dashboard_db),
):
    job_records = (
        db.query(models.Jobs)
        .order_by(models.Jobs.id.desc())
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="jobs.html",
        context={
            "page_title": "Jobs",
            "jobs": job_records,
        },
    )


# Applications page
@app.get("/frontend/applications", response_class=HTMLResponse)
async def applications_page(
    request: Request,
    db: Session = Depends(get_dashboard_db),
):
    application_records = (
        db.query(models.Applications)
        .order_by(models.Applications.id.desc())
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="applications.html",
        context={
            "page_title": "Applications",
            "applications": application_records,
        },
    )


# Interviews page
@app.get("/frontend/interviews", response_class=HTMLResponse)
async def interviews_page(
    request: Request,
    db: Session = Depends(get_dashboard_db),
):
    interview_records = (
        db.query(models.Interviews)
        .order_by(models.Interviews.id.desc())
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="interviews.html",
        context={
            "page_title": "Interviews",
            "interviews": interview_records,
        },
    )


# Contacts page
@app.get("/frontend/contacts", response_class=HTMLResponse)
async def contacts_page(
    request: Request,
    db: Session = Depends(get_dashboard_db),
):
    contact_records = (
        db.query(models.Contacts)
        .order_by(models.Contacts.id.desc())
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="contacts.html",
        context={
            "page_title": "Contacts",
            "contacts": contact_records,
        },
    )


# Login page
@app.get("/frontend/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={},
    )


# Process login form
@app.post("/frontend/login")
async def login_submit(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_dashboard_db),
):
    user = (
        db.query(models.Users)
        .filter(models.Users.email == username)
        .first()
    )

    if user is None or not auth.bcrypt_context.verify(
        password,
        user.hashed_password,
    ):
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={
                "error": "Invalid email or password"
            },
            status_code=401,
        )

    # Store the logged-in user's ID in the session
    request.session["user_id"] = user.id

    return RedirectResponse(
        url="/frontend",
        status_code=303,
    )


@app.get("/frontend/logout")
async def logout(request: Request):
    request.session.clear()

    return RedirectResponse(
        url="/frontend/login",
        status_code=303,
    )
