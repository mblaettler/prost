FROM python:3.12-slim

RUN pip install --no-cache-dir poetry

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-root

COPY backend/api/ ./api/
COPY backend/models/ ./models/

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]