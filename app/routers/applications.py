from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

import models
from dependencies import get_db, get_current_user
from schemas import ApplicationCreate, ApplicationResponse, ApplicationDashboard


router = APIRouter(prefix="/applications", tags=["Applications"])

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[int, Depends(get_current_user)]


@router.post("/", response_model=ApplicationResponse)
def create_application(
    application: ApplicationCreate,
    db: db_dependency,
    current_user: user_dependency
):
    job = db.query(models.Jobs).filter(
        models.Jobs.id == application.job_id
    ).first()

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    application_db = models.Applications(
        job_id=application.job_id,
        user_id=current_user,
        application_date=application.application_date,
        status=application.status,
        notes=application.notes
    )

    db.add(application_db)
    db.commit()
    db.refresh(application_db)

    return application_db

@router.get("/", response_model=list[ApplicationResponse])
def get_all_applications(
    db: db_dependency,
    current_user: user_dependency
):
    applications = db.query(models.Applications).filter(
        models.Applications.user_id == current_user
    ).all()

    return applications

@router.get("/dashboard", response_model=ApplicationDashboard)
def get_application_dashboard(
    db: db_dependency,
    current_user: user_dependency
):
    applications = db.query(models.Applications).filter(
        models.Applications.user_id == current_user
    ).all()

    total_applications = len(applications)

    applied = sum(
        1 for application in applications
        if application.status == "Applied"
    )

    interview = sum(
        1 for application in applications
        if application.status == "Interview"
    )

    rejected = sum(
        1 for application in applications
        if application.status == "Rejected"
    )

    offer = sum(
        1 for application in applications
        if application.status == "Offer"
    )

    return {
        "total_applications": total_applications,
        "applied": applied,
        "interview": interview,
        "rejected": rejected,
        "offer": offer
    }

@router.get("/status/{status}", response_model=list[ApplicationResponse])
def get_applications_by_status(
    status: str,
    db: db_dependency,
    current_user: user_dependency
):
    applications = db.query(models.Applications).filter(
        models.Applications.user_id == current_user,
        models.Applications.status == status
    ).all()

    return applications

@router.get("/limited", response_model=list[ApplicationResponse])
def get_limited_applications(
    db: db_dependency,
    current_user: user_dependency,
    page: int = 1,
    limit: int = 10
):
    skip = (page - 1) * limit

    applications = db.query(models.Applications).filter(
        models.Applications.user_id == current_user
    ).offset(skip).limit(limit).all()

    return applications

@router.get("/{application_id}", response_model=ApplicationResponse)
def get_application_by_id(
    application_id: int,
    db: db_dependency,
    current_user: user_dependency
):
    application = db.query(models.Applications).filter(
        models.Applications.id == application_id
    ).first()

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    if application.user_id != current_user:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to view this application"
        )

    return application

@router.put("/{application_id}", response_model=ApplicationResponse)
def update_application(
    application_id: int,
    application: ApplicationCreate,
    db: db_dependency,
    current_user: user_dependency
):
    application_db = db.query(models.Applications).filter(
        models.Applications.id == application_id
    ).first()

    if application_db is None:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    if application_db.user_id != current_user:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to update this application"
        )

    job = db.query(models.Jobs).filter(
        models.Jobs.id == application.job_id
    ).first()

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    application_db.job_id = application.job_id
    application_db.application_date = application.application_date
    application_db.status = application.status
    application_db.notes = application.notes

    db.commit()
    db.refresh(application_db)

    return application_db

@router.delete("/{application_id}")
def delete_application(
    application_id: int,
    db: db_dependency,
    current_user: user_dependency
):
    application = db.query(models.Applications).filter(
        models.Applications.id == application_id
    ).first()

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    if application.user_id != current_user:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to delete this application"
        )

    db.delete(application)
    db.commit()

    return {"message": "Application deleted successfully"}

