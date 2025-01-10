# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Expose the port your app runs on
EXPOSE 8000

# Set environment variable for SQLite database path (to match the shared volume)
# This assumes the SQLite database file will be located at /data/db.sqlite in the sqlite container's shared volume
ENV SQLITE_DB_PATH=/data/db.sqlite

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
