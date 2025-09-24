# Use an official Python runtime as a base image
FROM python:3.11-slim

# Install system dependencies, including the Rust compiler
RUN apt-get update && apt-get install -y --no-install-recommends `
    gcc `
    curl `
    && curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y `
    && apt-get clean `
    && rm -rf /var/lib/apt/lists/*

# Add Cargo's bin directory to the PATH
ENV PATH="/root/.cargo/bin:${PATH}"

# Set the working directory in the container
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port and run the application
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
