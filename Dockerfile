# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies (if any are needed, e.g., for Playwright if used later)
# RUN apt-get update && apt-get install -y --no-install-recommends some-package

# Copy requirements first to leverage Docker cache
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install --with-deps chromium

# Copy the rest of the application code
COPY ./app/templates /app/app/templates
COPY ./app /app/app
# COPY .env /app/.env # Copy .env file if it exists and you want it in the image
                    # For production, it's better to manage secrets outside the image

# Expose port 8000 (or whatever port your app runs on)
EXPOSE 8000

# Command to run the application using Uvicorn
# Gunicorn is often used in production as a process manager for Uvicorn workers
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
# Using gunicorn for better process management:
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-w", "2", "-b", "0.0.0.0:8000", "app.main:app"] 