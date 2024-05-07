# Use an official lightweight Python image
FROM python:3.11.3-slim

# Set the working directory in the Docker container
WORKDIR /app

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy the poetry lockfile and pyproject.toml into the container
COPY pyproject.toml poetry.lock* /app/

# Disable virtual environments as the container itself is isolated
RUN poetry config virtualenvs.create false

# Install dependencies using Poetry based on the lock file
RUN poetry install --no-dev  # Use --no-dev if you don't want dev dependencies

# Copy the rest of your application into the container
COPY . /app

# Expose the port the app runs on
EXPOSE 80

# Command to run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]
