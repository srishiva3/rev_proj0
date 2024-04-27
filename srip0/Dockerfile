# Start with a lightweight base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

RUN apt-get update && apt-get install -y sqlite3 libsqlite3-dev



# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the dependencies without caching to reduce image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Expose the port on which your FastAPI app will run
EXPOSE 8000

# Define the command to run FastAPI with Uvicorn
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
