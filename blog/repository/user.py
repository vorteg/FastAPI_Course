from sqlalchemy.orm import Session
from fastapi import status, HTTPException

from .. import models, schemas
from ..hashing import Hash


def create_user(request: schemas.User, db: Session):
    hashed_password = Hash.bcrypt(request.password)
    new_user = models.User(name=request.name, email=request.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def all(db: Session):
    users = db.query(models.User).all()
    return users


def get_user(id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with the id {id} is not available')
    return user


def user_by_email(email: str, request: schemas.Login, db: Session):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with the  {email} is not available')
    if not Hash.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Incorrect Password')
    return user
