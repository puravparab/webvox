# Webvox

Get audio summarizes for any website, blog or paper

## Prerequisites

- Docker
- Poetry

## Getting Started

1. Clone this repository:
	```
	git clone https://github.com/puravparab/webvox.git
	cd webvox
	```
2. Add environment variables to `notebooks/.env`
	```
	HF_TOKEN=
	```
3. Use Docker
   ```
   docker build -t webvox .
   docker run -p 8888:8888 -v $(pwd)/notebooks:/app/notebooks webvox
   ```
4. Use shell script
	```
	chmod +x run.sh
	./run.sh
	```

4. Run the jupyter notebook: [http://localhost:8888](http://localhost:8888)


## Project Structure

```
.
├── Dockerfile
├── notebooks/
│   └── main.ipynb
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