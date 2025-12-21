# Enercon RAG - Remote MCP Server
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements-remote.txt .
RUN pip install --no-cache-dir -r requirements-remote.txt

# Copy app files
COPY mcp_remote.py .
COPY pinecone_app_cloud.html .

# Cloud Run uses PORT env variable (default 8080)
EXPOSE 8080

# Run with PORT from environment
CMD exec uvicorn mcp_remote:app --host 0.0.0.0 --port ${PORT:-8080}
