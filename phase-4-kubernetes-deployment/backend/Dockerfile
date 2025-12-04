# Backend Dockerfile
FROM python:3.13-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy dependency files
COPY pyproject.toml README.md ./
COPY src ./src

# Install dependencies
RUN uv pip install --system -e ".[dev]"

# Fix file permissions for non-root user
RUN chmod -R 755 /app && \
    chown -R 1000:1000 /app

# Run as non-root user
USER 1000

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
