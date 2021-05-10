from datetime import timedelta
from fastapi import APIRouter, Depends
from .. import schemas, database, token
from sqlalchemy.orm import Session
from ..repository import user

ACCESS_TOKEN_EXPIRE_MINUTES = 30

get_db = database.get_db

router = APIRouter(
    tags=['Authentication']
)


@router.post('/login')
def login(request: schemas.Login, email: str, db: Session = Depends(get_db)):
    user_profile = user.user_by_email(email, request, db)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = token.create_access_token(data={"sub": user_profile.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
