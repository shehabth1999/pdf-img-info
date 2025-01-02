# Use the official Python 3.12.8 image from the Docker Hub as the base image
FROM python:3.12.8-slim

# Install system dependencies, including libmagic
RUN apt-get update && \
    apt-get install -y --no-install-recommends libmagic1 && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DJANGO_DEBUG=1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Install the dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire Django project into the container
COPY . /app/

# Expose port 8000 to make it available outside the container
EXPOSE 8000

# Set the default command to run the Django development server on port 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
