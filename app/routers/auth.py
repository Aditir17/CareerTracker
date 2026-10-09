from fastapi import APIRouter,HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Annotated

import models
from dependencies import get_db
from schemas import CreateUser, UserResponse

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

SECRET_KEY = "197b2c37c391bed93fe80344fe73b806947a65e36206e05a1a23c2fa12702fe3"
ALGORITHM = "HS256"

bcrypt_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

oauth2_bearer = OAuth2PasswordBearer(
    tokenUrl="auth/token"
)

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/")
def create_user(
    user: CreateUser,
    db: Session = Depends(get_db)
):
    db_user = models.Users(
        email=user.email,
        full_name=user.full_name,
        hashed_password=bcrypt_context.hash(user.password)
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

@router.get("/",response_model=list[UserResponse])
def get_user(db:db_dependency):
    users= db.query(models.Users).all()
    return users

@router.get("/{user_id}",response_model=UserResponse)
def get_user_by_id(user_id:int,db:db_dependency):

    user_by_id=db.query(models.Users).filter(models.Users.id==user_id).first()

    if user_by_id is None:
        raise HTTPException(status_code=404,detail="User not found")

    return user_by_id

@router.post("/token")
def login_for_access_token(db: db_dependency,form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.query(models.Users).filter(
        models.Users.email == form_data.username
    ).first()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    if not bcrypt_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    token = jwt.encode(
        {"sub": str(user.id)},
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {"access_token": token, "token_type": "bearer"}
