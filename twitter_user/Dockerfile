FROM python:3.12

RUN apt-get update && apt-get install -y \
    && pip install poetry

WORKDIR /twitter_user

COPY pyproject.toml poetry.lock ./
COPY . .

RUN poetry config virtualenvs.in-project true \
    && poetry install --no-interaction --no-ansi
    
ENTRYPOINT ["poetry", "run", "python", "collect_executor.py"]
