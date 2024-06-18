FROM python:3.12

RUN apt-get update && apt-get install -y \
    && pip install poetry

WORKDIR /amazon_product

COPY pyproject.toml ./

RUN poetry config virtualenvs.in-project true \
    && poetry install --no-interaction --no-ansi

COPY . .

ENTRYPOINT ["poetry", "run", "python", "collect_executor.py"]