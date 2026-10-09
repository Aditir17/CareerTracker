from fastapi import Depends,HTTPException
from jose import jwt, JWTError

from database import SessionLocal
from fastapi.security import OAuth2PasswordBearer

def get_db():
    db=SessionLocal()

    try:
        yield db
    finally:
        db.close()

oauth2_bearer = OAuth2PasswordBearer(
    tokenUrl="auth/token"
)

SECRET_KEY = "197b2c37c391bed93fe80344fe73b806947a65e36206e05a1a23c2fa12702fe3"
ALGORITHM = "HS256"

def get_current_user(token:str=Depends(oauth2_bearer)):
    try:
        payload=jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id=payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code=401,detail="Could not validate user")
        return int(user_id)

    except JWTError:
        raise HTTPException(status_code=401,detail="Could not validate user")



