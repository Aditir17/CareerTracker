from fastapi import FastAPI, Depends, HTTPException,Query
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker, Session
from typing import Annotated

import models
from database import engine, Base
from dependencies import get_db
from routers import companies,jobs,interviews,auth, contacts, applications
from schemas import CreateUser, UserResponse, CompanyCreate, CompanyResponse, JobResponse, JobCreate, InterviewResponse, \
    InterviewCreate

app=FastAPI(
    title="CareerTrack API",
    description="Job Application & Recruiter Follow-up Platform",
    version="1.0.0"
)

app.include_router(companies.router)
app.include_router(jobs.router)
app.include_router(interviews.router)
app.include_router(auth.router)
app.include_router(contacts.router)
app.include_router(applications.router)

models.Base.metadata.create_all(bind=engine)







