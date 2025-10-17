# Use official Python slim image
FROM python:3.12-slim

# Set workdir
WORKDIR /app

# Avoid buffering
ENV PYTHONUNBUFFERED=1

# Copy requirements first and install to leverage Docker cache
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy package
COPY . /app

# Expose port
EXPOSE 8080

# Default command: run uvicorn
CMD ["python", "-m", "uvicorn", "mcp_server.http_api:app", "--host", "0.0.0.0", "--port", "8080"]
