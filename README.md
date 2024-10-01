# Webvox

Get audio summarizes for any website, blog or paper

## Prerequisites

- Docker
- Poetry

## Getting Started

1. Clone this repository:
	```
	git clone https://github.com/puravparab/webvox.git
	```
	or
	```
	git clone git@github.com:puravparab/webvox.git
	```
	```
	cd webvox
	```

2. Build the Docker image:
   ```
   docker build -t webvox .
   ```

3. Run the Docker container:
   ```
   docker run -p 8888:8888 -v $(pwd)/notebooks:/app/notebooks webvox
   ```

4. Run the jupyter notebook: [http://localhost:8888](http://localhost:8888)


## Project Structure

```
.
├── Dockerfile
├── pyproject.toml
├── poetry.lock
├── notebooks/
│   └── ... (your Jupyter notebooks)
└── README.md
```

## Adding Dependencies

To add new dependencies to the project:

1. Locally:
   ```
   poetry add package-name
   ```

2. Rebuild the Docker image to reflect changes:
   ```
   docker build -t webvox .
   ```