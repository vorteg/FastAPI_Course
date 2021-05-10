from typing import Optional
from pydantic import BaseModel

from fastapi import FastAPI


app = FastAPI()

@app.get('/blog')
def index(limit: int = 10, published: bool = True, sort:Optional[str] = None):
    # only get 10 published blogs
    if published:
        return {'data':f'{limit} published blogs from the db'}
    else:
        return {'data':f'{limit} published from the db'}


@app.get('/blog/unpublished')
def unpublished():
    # Remeber that this function allows 
    # a dinamic route vs "/blog/{id}"
    return {'data': 'all  unpublished blogs'}


@app.get('/blog/{id}')
def show(id: int):

    # Fetch blog with id = id

    return {'data': id}


@app.get('/blog/{id}/comments')
def commments(id: int, limit=10):

    # fetch comments of blog with id = id 
    # fastApi is smart and automaticlly way reconoize the query paramms
    return {'data':  {'1', '2'}}


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]

@app.post('/blog')
def create_blog(request: Blog):
    return {'data': f'Blog created with title as {request.title}'}
    

