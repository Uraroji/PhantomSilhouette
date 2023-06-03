FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1
EXPOSE 8000
WORKDIR /app

RUN apt update && apt install -y build-essential ca-certificates libsndfile1
COPY poetry.lock pyproject.toml ./
RUN pip install poetry==1.2.2 && \
    poetry config virtualenvs.create false && \
    poetry add gunicorn && \
    poetry install --no-dev

WORKDIR /app
COPY ./static ./static
COPY ./PhantomSilhouette.py ./PhantomSilhouette.py
COPY ./app.py ./app.py
COPY ./LICENCE ./LICENCE

CMD gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 app:app