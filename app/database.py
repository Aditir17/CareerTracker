from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL="postgresql+psycopg://postgres:aditilohokare17@localhost:5432/careertrack"

engine=create_engine(DATABASE_URL)

SessionLocal=sessionmaker(autocommit= False,autoflush=False, bind=engine)

Base=declarative_base()