#!/bin/bash

cd notebooks

check_error() {
	if [ $? -ne 0 ]; then
		echo "Error: $1"
		exit 1
	fi
}

mkdir -p models
check_error "Failed to create models directory"

mkdir -p outputs
check_error "Failed to create outputs directory"

# Clone MeloTTS repository if it doesn't exist
if [ ! -d "models/MeloTTS" ]; then
	echo "Cloning MeloTTS repository..."
	git clone https://github.com/myshell-ai/MeloTTS.git models/MeloTTS
	check_error "Failed to clone MeloTTS repository"
else
	echo "MeloTTS repository already exists, skipping clone"
fi

# Build the Docker image
echo "Building Docker image..."
docker build -t webvox .
check_error "Failed to build Docker image"

# Run the Docker container
echo "Running Docker container..."
docker run -p 8888:8888 \
			-v "$(pwd):/app" \
			-v "$(pwd)/outputs:/app/outputs" \
			-v "$(pwd)/models:/app/models" \
			webvox
check_error "Failed to run Docker container"