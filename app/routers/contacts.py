from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

import models
from dependencies import get_db
from schemas import ContactCreate, ContactResponse

router = APIRouter(
    prefix="/contacts",
    tags=["Contacts"]
)

db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/", response_model=ContactResponse)
def create_contact(
    contact: ContactCreate,
    db: db_dependency
):
    company = db.query(models.Companies).filter(
        models.Companies.id == contact.company_id
    ).first()

    if company is None:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    db_contact = models.Contacts(
        name=contact.name,
        email=contact.email,
        phone=contact.phone,
        designation=contact.designation,
        company_id=contact.company_id
    )

    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)

    return db_contact

@router.get("/", response_model=list[ContactResponse])
def get_all_contacts(db: db_dependency):
    contacts = db.query(models.Contacts).all()

    return contacts

@router.get("/{contact_id}", response_model=ContactResponse)
def get_contact_by_id(
    contact_id: int,
    db: db_dependency
):
    contact = db.query(models.Contacts).filter(
        models.Contacts.id == contact_id
    ).first()

    if contact is None:
        raise HTTPException(
            status_code=404,
            detail="Contact not found"
        )

    return contact

@router.put("/{contact_id}", response_model=ContactResponse)
def update_contact(
    contact_id: int,
    contact: ContactCreate,
    db: db_dependency
):
    contact_db = db.query(models.Contacts).filter(
        models.Contacts.id == contact_id
    ).first()

    if contact_db is None:
        raise HTTPException(
            status_code=404,
            detail="Contact not found"
        )

    company = db.query(models.Companies).filter(
        models.Companies.id == contact.company_id
    ).first()

    if company is None:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    contact_db.name = contact.name
    contact_db.email = contact.email
    contact_db.phone = contact.phone
    contact_db.designation = contact.designation
    contact_db.company_id = contact.company_id

    db.commit()
    db.refresh(contact_db)

    return contact_db

@router.delete("/{contact_id}")
def delete_contact(
    contact_id: int,
    db: db_dependency
):
    contact = db.query(models.Contacts).filter(
        models.Contacts.id == contact_id
    ).first()

    if contact is None:
        raise HTTPException(
            status_code=404,
            detail="Contact not found"
        )

    db.delete(contact)
    db.commit()

    return {"message": "Contact deleted successfully"}