#!/bin/bash

check_error() {
	if [ $? -ne 0 ]; then
		echo "Error: $1"
		exit 1
	fi
}

# Build the Docker image
echo "Building Docker image..."
docker build -t webvox .
check_error "Failed to build Docker image"

# Run the Docker container
echo "Running Docker container..."
docker run -p 8888:8888 -v "$(pwd)/notebooks:/app/notebooks" webvox
check_error "Failed to run Docker container"