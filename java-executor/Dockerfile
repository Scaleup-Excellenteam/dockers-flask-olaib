# Use Alpine Linux as the base image
FROM alpine:latest

# Install OpenJDK and Python
RUN apk add --no-cache openjdk11 python3 py3-pip

# Set the working directory
WORKDIR /app

RUN apk add --no-cache libc-dev


# Copy the Flask application code into the container
COPY . /app

# Install Flask and other dependencies
RUN pip install flask

# Start the Flask application
CMD ["python3", "app.py"]