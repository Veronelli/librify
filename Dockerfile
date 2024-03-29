# Use the official Python 3.11-alpine base image
FROM python:3.11-alpine

# Set the working directory inside the container
WORKDIR /app

# Install git
RUN apk add git

# Install system dependencies needed for building Python packages and virtualenv
RUN apk add --no-cache build-base libffi-dev openssl-dev python3-dev

ENV VIRTUAL_ENV=/venv
RUN python3.11 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install --no-cache-dir uvicorn


# Activate the virtual environment
ENV PATH="/venv/bin:$PATH"

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy the pyproject.toml and poetry.lock files to the working directory
COPY pyproject.toml poetry.lock ./

# Install project dependencies using Poetry within the virtual environment
RUN poetry config virtualenvs.create true \
    && poetry install --no-root --no-dev

# Copy the entire project directory (assuming it's in the same directory as the Dockerfile) to the working directory
COPY . .

# Expose the port on which the FastAPI application will run (change it to the appropriate port used by your FastAPI app)
EXPOSE 8000

# Start the FastAPI application with live reloading using Uvicorn
CMD uvicorn main:app --reload --host 0.0.0.0 --port 8000