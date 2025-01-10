# Use an official Python runtime as a parent image
FROM python:3.10

# Install the required CA certificates and OpenSSL
RUN apt-get update && apt-get install -y ca-certificates openssl && update-ca-certificates

# Set the working directory
WORKDIR /app

# Copy requirements.txt
COPY requirements.txt .

# Install dependencies with trusted hosts to avoid SSL errors
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org -r requirements.txt

# Copy the FastAPI app code to the container
COPY . /app/

# Expose port (default FastAPI port)
EXPOSE 8000

# Command to run FastAPI with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
