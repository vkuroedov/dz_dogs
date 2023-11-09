from enum import Enum
from fastapi import FastAPI, HTTPException
from fastapi import param_functions
from pydantic import BaseModel

app = FastAPI()

class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


@app.get('/', summary='Root')
def root():
    return {'Hello'}

@app.post('/post')
def post():
    pass

@app.get('/dog', summary='Get Dogs')
def get_dog(kind: DogType):
    return dogs_db[DogType.kind]

@app.get('/dog/{pk}', summary='Get Dog By Pk')
def get_dogs_by_pk(pk: int):
    return dogs_db[pk]

@app.post('/dog', response_model=Dog, summary='Create Dog')
def create_dog(dog: Dog):
    existing_pk = ...
    if existing_pk:
        raise HTTPException(status_code=409,
                            detail='The specified PK already exists.')
    
    ...

    return Dog(...)
