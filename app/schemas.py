from datetime import datetime, date

from pydantic import BaseModel

class CreateUser(BaseModel):
    email:str
    full_name:str
    password:str


class UserResponse(BaseModel):
    id:int
    email:str
    full_name:str

    class Config:
        from_attributes = True

class CompanyCreate(BaseModel):
    name:str
    website:str

class CompanyResponse(BaseModel):
    id:int
    name:str
    website:str
    user_id:int

    class Config:
        from_attributes =True


class JobCreate(BaseModel):
    title:str
    description:str
    location:str
    company_id:int
    status:str

class JobResponse(BaseModel):
    id:int
    title: str
    description: str
    location: str
    company_id: int
    status:str

    class Config:
        from_attributes=True

class InterviewCreate(BaseModel):
    job_id: int
    interview_date: datetime
    interview_type: str
    notes: str


class InterviewResponse(BaseModel):
    id: int
    job_id: int
    interview_date: datetime
    interview_type: str
    notes: str


    class Config:
        from_attributes = True

class ContactCreate(BaseModel):
    name: str
    email: str
    phone: str
    designation: str
    company_id: int


class ContactResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    designation: str
    company_id: int

    class Config:
        from_attributes = True

class ApplicationCreate(BaseModel):
    job_id: int
    application_date: date
    status: str
    notes: str


class ApplicationResponse(BaseModel):
    id: int
    job_id: int
    user_id: int
    application_date: date
    status: str
    notes: str

    class Config:
        from_attributes = True

class ApplicationDashboard(BaseModel):
    total_applications: int
    applied: int
    interview: int
    rejected: int
    offer: int