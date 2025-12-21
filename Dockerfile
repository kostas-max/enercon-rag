# Enercon RAG - Remote MCP Server
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements-remote.txt .
RUN pip install --no-cache-dir -r requirements-remote.txt

# Copy app
COPY mcp_remote.py .

# Port (Cloud Run uses PORT env variable)
ENV PORT=8080

# Run
CMD ["sh", "-c", "uvicorn mcp_remote:app --host 0.0.0.0 --port $PORT"]
