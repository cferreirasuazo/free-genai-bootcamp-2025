# Use Python 3.12 slim image as base
FROM python:3.12-slim-bookworm

# Copy UV (fast package manager) from Astral's repository
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory inside the container
WORKDIR /app

# Copy project files
COPY . .

# Create and activate virtual environment, then install dependencies
RUN uv venv && uv pip install -r requirements.txt

# Expose port 8000 for FastAPI
EXPOSE 8000

# Ensure virtual environment binaries are in PATH
ENV PATH="/app/.venv/bin:$PATH"

# Run the application with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
