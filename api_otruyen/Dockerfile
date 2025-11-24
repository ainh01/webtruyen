# Base image (slim for smaller size)
FROM python:3.11-slim

# Prevent Python from writing pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# 1. Dependency Layer (Cached if requirements.txt doesn't change)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. Code Layer
COPY . .

# 3. Security: Run as non-root user
RUN adduser --disabled-password --gecos '' appuser
USER appuser

# 4. Run (Host must be 0.0.0.0 for Docker)
EXPOSE 8001
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
