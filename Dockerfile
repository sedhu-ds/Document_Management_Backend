

FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app code
COPY . .

# Set environment variables (consider using ARG or pass them via docker run)
ENV DATABASE_URL=postgresql://admin:your-password@<rds-endpoint>:5432/doc_management
ENV SECRET_KEY=<your-secret-key>

# Expose the port your app runs on
EXPOSE 8000

# Use exec form and recommend adding reload only for dev environments
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]



# FROM python:3.9

# WORKDIR /app

# # Install build dependencies for gevent and other C extensions (ARM64/M1/M2 compatible)
# RUN apt-get update && apt-get install -y gcc g++ build-essential libc-dev && rm -rf /var/lib/apt/lists/*

# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 