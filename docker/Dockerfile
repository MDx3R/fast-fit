FROM python:3.11-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root

COPY cli ./cli
COPY src ./src
COPY templates ./templates
COPY static ./static
COPY configs ./configs

CMD ["poetry", "run", "uvicorn", "cli.app:app", "--host", "0.0.0.0", "--port", "8000"]