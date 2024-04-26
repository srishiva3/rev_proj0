# Use the official Python image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI app code into the container
COPY . .

# Expose port 8000 for FastAPI
EXPOSE 8000

# Command to start FastAPI with Uvicorn
CMD ["uvicorn", "your_fastapi_file:app", "--host", "0.0.0.0", "--port", "8000"]
