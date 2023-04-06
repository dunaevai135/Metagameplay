# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN python -m grpc_tools.protoc -I./proto --python_out=. --pyi_out=. --grpc_python_out=. ./proto/metagameplay.proto

# Make sure the scripts are executable
RUN chmod +x client.py
RUN chmod +x serv.py

EXPOSE 50051

# Run script1.py when the container starts
CMD ["python", "serv.py"]
