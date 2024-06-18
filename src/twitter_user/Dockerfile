FROM python:3.12

RUN apt-get update && apt-get install -y \
    && pip install poetry

WORKDIR /twitter_user

COPY pyproject.toml ./

RUN poetry install

COPY . .

ENTRYPOINT ["poetry", "run", "python", "collect_executor.py"]