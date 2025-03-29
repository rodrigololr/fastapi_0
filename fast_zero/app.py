from fastapi import FastAPI
from http import HTTPStatus
from fast_zero.schemas import UserSchema, UserPublic, UserDB

app = FastAPI()

database = []  # banco de dados provisorio apenas para testes


@app.get('/')
def read_root():
    return {'message': 'Olá lucas !'}


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):

    user_with_id = UserDB(**user.model_dump(), id=len(database) + 1)
    # ta convertendo um objeto do pydantic em dicionario (o **user.model_dump)
    # no caso oq ta fazendo é pegando user com as info e colocando e um dicionario json

    database.append(user_with_id)

    return user_with_id
