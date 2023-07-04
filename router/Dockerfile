# Use Alpine Linux as the base image
FROM python:3.9-alpine

# Set the working directory
WORKDIR /app

# Copy the Flask application code into the container
COPY . /app

# Install Flask and other dependencies
RUN pip install flask
RUN pip install requests

# Start the Flask application
CMD ["python", "app.py"]