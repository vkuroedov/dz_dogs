from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

#comment

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

# возвращает строку
@app.get('/', summary='Root')
def root():
    return {'Hello'}

# добавляем объект в post_db, который на +1 отличается от предыдущего объекта
@app.post('/post',response_model=Timestamp, summary='Get Post')
def post():
    post_db.append(Timestamp(id=post_db[-1].id + 1, timestamp=post_db[-1].timestamp + 1))
    return {
        'id': post_db[-1].id,
        'timestamp': post_db[-1].timestamp
    }

# вытасикваем собакенов по породе. Если порода не указана - вытаскиваем всех собакенов
@app.get('/dog', response_model=List[Dog], summary='Get Dogs')
def get_dog(kind: DogType = None):
    if kind is None:
        return dogs_db.values()
    else:
        return [i for i in dogs_db.values() if i.kind == kind]

# добавляем собакена в базу данных. Если собака с таким pk уже существует - выкидываем 409
# тут и далее считаем, что pk и ключ dogs_db должны быть равны и уникальны
@app.post('/dog', response_model=Dog, summary='Create Dog')
def create_dog(dog: Dog):
    if dog.pk in [i.pk for i in dogs_db.values()]:
        raise HTTPException(status_code=409, detail='The specified PK already exists')
    else:
        dogs_db.update({dog.pk: dog})
        return dog

# ищем собакена по pk. Если записи с таким PK не существует - возвращаем 409
@app.get('/dog/{pk}', response_model=Dog, summary='Get Dog By Pk')
def get_dog_by_pk(pk: int):
    if len([i for i in dogs_db.values() if i.pk == pk]) == 0:
        raise HTTPException(status_code=409, detail='No such PK in database')
    else:
        return [i for i in dogs_db.values() if i.pk == pk][0]
    
# апдетйим собакена по PK. Если такого РК не существует - возвращаем 409 
# pk в ручке - текущий pk собаки, информацию о которой хотим обновить
# pk в request_body - новый pk собаки (поменяла паспорт при достижении 14 лет)
@app.patch('/dog/{pk}', response_model=Dog, summary='Update Dog')
def create_dog(pk: int, dog: Dog):
    if pk not in dogs_db.keys():
        raise HTTPException(status_code=409, detail='No such PK in database')
    else:
        del dogs_db[pk] # удаляем запись по текущему pk
        dogs_db.update({dog.pk: dog}) #добавление записи с новыми атрибутами
        return dog
