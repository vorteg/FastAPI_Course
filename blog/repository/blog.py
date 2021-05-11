from sqlalchemy.orm import Session
from fastapi import status, HTTPException

from .. import models, schemas



def get_all(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs

def show(id:int,  db:Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f'Blog with the id {id} is not available')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return{'detail':f'Blog with the id {id} is not available'}
    return blog

def create(request: schemas.Blog, db:Session, id:int):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def destroy(id:int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with id {id} not found')    
    blog.delete(synchronize_session=False)
    db.commit()
    #return 'done'

def update(id:int, request: schemas.Blog, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with id {id} not found')
    blog.update({'title':request.title}) 
    # Para actalizar por esquemas es con blog.update(request)
    db.commit()
    return 'updated'