FROM python:3.12

RUN apt-get update && apt-get install -y \
    && pip install poetry

WORKDIR /amazon_product

COPY pyproject.toml poetry.lock ./
COPY . .

RUN poetry config virtualenvs.in-project true \
    && poetry install --no-interaction --no-ansi

ENTRYPOINT ["python", "collect_executor.py"]
