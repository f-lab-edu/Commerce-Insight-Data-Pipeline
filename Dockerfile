FROM python:3.12

RUN apt-get update && apt-get install -y \
    && pip install poetry

WORKDIR ./

COPY pyproject.toml poetry.lock ./
COPY app ./app

RUN poetry config virtualenvs.in-project true \
    && poetry install --no-interaction --no-ansi
    
EXPOSE 8000
ENTRYPOINT [ "poetry" ,"run", "uvicorn", "main:app", "--host", "0.0.0.0" ]