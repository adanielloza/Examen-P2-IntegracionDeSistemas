FROM python:3.11-slim
WORKDIR /app

# Spyne is a WSGI SOAP framework
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the WSGI entrypoint
COPY app ./app

# Expose SOAP port
EXPOSE 8006

# Run the built-in WSGI server
CMD ["python", "app/main.py"]
