FROM python:3.12-slim

RUN pip install --no-cache-dir poetry

WORKDIR /app

COPY pyproject.toml poetry.lock README.md ./
COPY api/ ./api/
COPY models/ ./models/
RUN poetry config virtualenvs.create false \
    && poetry install --only main

COPY entrypoint.sh ./
RUN chmod +x entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]