from datetime import timedelta
from fastapi import APIRouter, Depends
from .. import database, token, schemas
from sqlalchemy.orm import Session
from ..repository import user
from fastapi.security import OAuth2PasswordRequestForm

ACCESS_TOKEN_EXPIRE_MINUTES = 30

get_db = database.get_db

router = APIRouter(
    tags=['Authentication']
)


@router.post('/login', response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), email: str = None, db: Session = Depends(get_db)):
    user_profile = user.user_by_username(form_data, db)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = token.create_access_token(data={"sub": user_profile.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
