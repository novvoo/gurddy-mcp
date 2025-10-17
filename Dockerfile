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

# Install the package
RUN pip install --no-cache-dir -e .

# Expose port for MCP HTTP server
EXPOSE 8080

# Default command: run MCP HTTP server
CMD ["python", "-m", "uvicorn", "mcp_server.mcp_http_server:app", "--host", "0.0.0.0", "--port", "8080"]
