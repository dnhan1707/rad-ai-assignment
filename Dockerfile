FROM python:3.12-alpine

WORKDIR /app

COPY requirements-dev.txt requirements.txt ./

RUN pip install --no-cache-dir -r requirements-dev.txt

COPY src/ ./src/
COPY tests/ ./tests/


CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]