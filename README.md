# Webvox

Get audio summarizes for any website, blog or paper

## Prerequisites

- Docker

## Setup

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
  docker run -p 8888:8888 -v $(pwd)/notebooks:/app/notebooks -v $(pwd)/models:/app/models webvox
   ```
4. Use shell script
	```
	chmod +x run.sh
	./run.sh
	```

4. Run the jupyter notebook: [http://localhost:8888/main.ipynb](http://localhost:8888)


## Project Structure

```
webvox
├── Dockerfile
├── models/
├── notebooks/
│   └── main.ipynb
├── notebooks/
└── README.md
```

## Adding Dependencies

Add them to requirements.txt