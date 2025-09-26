# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the FastAPI port
EXPOSE 8000

# Run FastAPI with uvicorn
CMD ["uvicorn", "aap:app", "--host", "0.0.0.0", "--port", "8000"]
