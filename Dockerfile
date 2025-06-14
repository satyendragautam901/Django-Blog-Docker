# Use a lightweight base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Prevent Python from generating .pyc files
ENV PYTHONUNBUFFERED 1

# Install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Run migrations and collect static files (if applicable)
# Uncomment if you need these
# RUN python manage.py migrate
# RUN python manage.py collectstatic --noinput

# Command to start the application
CMD python manage.py runserver 0.0.0.0:8000
