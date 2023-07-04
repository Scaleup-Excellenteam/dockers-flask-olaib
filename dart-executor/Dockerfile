FROM alpine:latest

#RUN apk update && apk add bash curl git
#RUN curl --location https://dart.dev/getSdk | bash

# Set the working directory
WORKDIR /app

# Copy the Flask application code into the container
COPY . /app

# Install Flask and other dependencies
RUN pip install flask

# Run the Flask application
CMD ["python", "app.py"]
