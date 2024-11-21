FROM python:3.12-alpine

RUN pip install poetry==1.8.4

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install

COPY . .

ENTRYPOINT ["poetry", "run", "python", "main.py"]