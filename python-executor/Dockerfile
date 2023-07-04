# Use Alpine Linux as the base image
FROM python:3.9-alpine

# Set the working directory
WORKDIR /app

# Copy the Flask application code into the container
COPY . /app

RUN pip install flask

# Start the Flask application
CMD ["python", "app.py"]
