from fastapi import APIRouter, HTTPException, Depends,Query
from sqlalchemy.orm import Session
from typing import Annotated
from datetime import datetime

import models
from dependencies import get_db
from schemas import InterviewResponse,InterviewCreate

router = APIRouter(
    prefix="/interviews",
    tags=["Interviews"]
)

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/",response_model=InterviewResponse)
def create_interview(interview:InterviewCreate,db:db_dependency):
    new_interview=models.Interviews(
        job_id=interview.job_id,
        interview_date=interview.interview_date,
        interview_type=interview.interview_type,
        notes=interview.notes
    )

    db.add(new_interview)
    db.commit()
    db.refresh(new_interview)

    return new_interview

@router.get("/",response_model=list[InterviewResponse])
def get_all_interviews(db:db_dependency):
    interviews=db.query(models.Interviews).all()

    return interviews

@router.get("/{interview_id}",response_model=InterviewResponse)
def get_interview_by_id(interview_id:int,db:db_dependency):
    interview=db.query(models.Interviews).filter(models.Interviews.id==interview_id).first()

    if interview is None:
        raise HTTPException(status_code=404,detail="Interview not found")
    return interview

@router.put("/{interview_id}",response_model=InterviewResponse)
def update_interview_by_id(interview_id:int,db:db_dependency,interview:InterviewCreate):
    interview_db = db.query(models.Interviews).filter(models.Interviews.id == interview_id).first()

    if interview_db is None:
        raise HTTPException(status_code=404, detail="Interview not found")

    interview_db.job_id = interview.job_id
    interview_db.interview_date = interview.interview_date
    interview_db.interview_type = interview.interview_type
    interview_db.notes = interview.notes

    db.commit()
    db.refresh(interview_db)

    return interview_db

@router.delete("/{interview_id}")
def delete_interview_by_id(interview_id:int,db:db_dependency):
    interview=db.query(models.Interviews).filter(models.Interviews.id==interview_id).first()

    if interview is None:
        raise HTTPException(status_code=404,detail="Interview not found")

    db.delete(interview)
    db.commit()
    return {"message": "Interview deleted successfully"}

