from fastapi import APIRouter, HTTPException, Depends,Query
from sqlalchemy.orm import Session
from typing import Annotated

from app import models
from app.dependencies import get_db, get_current_user
from app.schemas import JobCreate, JobResponse, InterviewResponse

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency=Annotated[int,Depends(get_current_user)]

@router.post("/",response_model=JobResponse)
def create_job(job:JobCreate,db:db_dependency,
               current_user:user_dependency):

    company = db.query(models.Companies).filter(
        models.Companies.id == job.company_id
    ).first()

    if company is None:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    if company.user_id != current_user:
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this company"
        )
    job_db=models.Jobs(
        title=job.title,
        description=job.description,
        location=job.location,
        company_id=job.company_id,
        status=job.status
    )

    db.add(job_db)
    db.commit()
    db.refresh(job_db)

    return job_db


@router.get("/", response_model=list[JobResponse])
def get_all_jobs(
    db: db_dependency,
    current_user: user_dependency
):
    jobs = db.query(models.Jobs).all()
    return jobs

@router.put("/{job_id}",response_model=JobResponse)
def update_job_by_id(job_id:int,job:JobCreate,db:db_dependency):

    job_db=db.query(models.Jobs).filter(models.Jobs.id==job_id).first()

    if job_db is None:
        raise HTTPException(status_code=404, detail="Job not found")

    job_db.title=job.title
    job_db.description=job.description
    job_db.location=job.location
    job_db.company_id=job.company_id
    job_db.status = job.status

    db.commit()
    db.refresh(job_db)
    return job_db

@router.delete("/{job_id}")
def delete_job_by_id(
    job_id: int,
    db: db_dependency,
    current_user: user_dependency
):
    job = db.query(models.Jobs).filter(
        models.Jobs.id == job_id
    ).first()

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    company = db.query(models.Companies).filter(
        models.Companies.id == job.company_id
    ).first()

    if company is None:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    if company.user_id != current_user:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to delete this job"
        )

    db.delete(job)
    db.commit()

    return {"message": "Job deleted successfully"}

