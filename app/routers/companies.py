from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Annotated

import models
from dependencies import get_db, get_current_user
from schemas import CompanyCreate, CompanyResponse, JobResponse
from routers.auth import oauth2_bearer

router=APIRouter(prefix="/companies",tags=["Companies"])

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency=Annotated[int,Depends(get_current_user)]

@router.post("/", response_model=CompanyResponse)
def create_company(company: CompanyCreate, db: db_dependency,
                   current_user:user_dependency):

    company = models.Companies(
        name = company.name,
        website= company.website,
        user_id=current_user

    )
    db.add(company)
    db.commit()
    db.refresh(company)

    return company

@router.get("/",response_model=list[CompanyResponse])
def get_all_companies(db: db_dependency,
            current_user:user_dependency
                      ):
    companies=db.query(models.Companies).filter(models.Companies.user_id==current_user).all()
    return companies

@router.get("/{company_id}",response_model=CompanyResponse)
def get_company_by_id(company_id:int,db:db_dependency):
    company=db.query(models.Companies).filter(models.Companies.id==company_id).first()

    if company is None:
        raise HTTPException(status_code=404,detail="Company not found")

    return company

@router.put("/{company_id}",response_model=CompanyResponse)
def update_company_by_id(company_id:int,company:CompanyCreate,db:Session=Depends(get_db)):
    company_db=db.query(models.Companies).filter(models.Companies.id==company_id).first()

    if company_db is None:
        raise HTTPException(status_code=404, detail="Company not found")

    company_db.name=company.name
    company_db.website=company.website
    company_db.user_id=company.user_id

    db.commit()
    db.refresh(company_db)
    return company_db

@router.delete("/{company_id}")
def delete_company(
    company_id: int,
    db: db_dependency,
    current_user: user_dependency
):
    company = db.query(models.Companies).filter(
        models.Companies.id == company_id
    ).first()

    if company is None:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    if company.user_id != current_user:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to delete this company"
        )

    db.delete(company)
    db.commit()

    return {"message": "Company deleted successfully"}

@router.get("/{company_id}/jobs",response_model=list[JobResponse])
def get_all_jobs_by_company_id(company_id:int,db:db_dependency):
    company = db.query(models.Companies).filter(models.Companies.id == company_id).first()

    if company is None:
        raise HTTPException(status_code=404,detail="Company not found")

    return company.jobs