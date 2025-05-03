FROM python:3.13-slim
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR app/
COPY . .

RUN pip install poetry

RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi

EXPOSE 8000
CMD poetry run uvicorn --host 0.0.0.0 fast_zero.app:app

#cria a imagem
# docker build -t "fast_zero" .

# inicia a imagem
#docker run -it --name fastzeroapp -p 8000:8000 fast_zero:latest

# remove o containe
# docker rm fastzeroapp

#pra ver os dockers
# docker ps'