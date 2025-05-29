# Use a slim Python base
FROM python:3.11-slim

# Set a working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy our code
COPY app ./app

# Expose the port your FastAPI runs on
EXPOSE 8005

# Launch with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8005"]
