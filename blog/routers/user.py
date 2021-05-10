from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from .. import schemas, database
from ..repository import user

router = APIRouter(
    prefix='/user',
    tags=['users']
)

get_db = database.get_db


@router.post('', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return user.create_user(request, db)


@router.get('', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowUser])
def all(db: Session = Depends(get_db)):
    return user.all(db)


@router.get('/{id}', response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(get_db)):
    return user.get_user(id, db)
