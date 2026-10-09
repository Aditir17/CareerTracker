from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy import DateTime

from database import Base

class Users(Base):
    __tablename__="users"

    id=Column(Integer,primary_key=True, index=True)
    full_name=Column(String,unique=True, index=True)
    email=Column(String)
    hashed_password=Column(String)

    applications = relationship("Applications", back_populates="user")

class Companies(Base):
    __tablename__="companies"

    id=Column(Integer,primary_key=True,index=True)
    name=Column(String)
    website=Column(String)
    user_id=Column(Integer,ForeignKey("users.id"))

    jobs=relationship("Jobs",back_populates="company")
    contacts = relationship("Contacts", back_populates="company")

class Jobs(Base):
    __tablename__="jobs"

    id=Column(Integer,primary_key=True,index=True)
    title=Column(String)
    description=Column(String)
    location=Column(String)
    company_id=Column(Integer,ForeignKey("companies.id"))
    status = Column(String)

    company = relationship("Companies",back_populates="jobs")
    interviews = relationship("Interviews", back_populates="job")
    applications = relationship("Applications", back_populates="job")

class Interviews(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    interview_date = Column(DateTime)
    interview_type = Column(String)
    notes = Column(String)

    job = relationship("Jobs", back_populates="interviews")

class Contacts(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    designation = Column(String)
    company_id = Column(Integer, ForeignKey("companies.id"))

    company = relationship("Companies", back_populates="contacts")

class Applications(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    application_date = Column(Date)
    status = Column(String)
    notes = Column(String)

    job = relationship("Jobs", back_populates="applications")
    user = relationship("Users", back_populates="applications")
