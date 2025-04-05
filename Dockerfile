# Build stage
FROM python:3.9 as builder
WORKDIR /app
COPY app/requirements.txt .
RUN python -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"
RUN pip install -r requirements.txt

# Runtime stage
FROM python:3.9-slim
WORKDIR /app
COPY --from=builder /app/venv /app/venv
ENV PATH="/app/venv/bin:$PATH"
COPY app/ .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]