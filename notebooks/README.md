# Webvox Notebooks

Notebooks provide a guide for scraping, text summarization and text-to-speech generation

## Setup

1. Add environment variables to a `.env` file
	```
	HF_TOKEN=
	```
2. Clone the MeloTTS repo
```
cd models
git clone https://github.com/myshell-ai/MeloTTS.git
cd ..
```
3. Build and run Docker
	```
	docker build -t webvox .
	docker run -p 8888:8888 -v "$(pwd):/app" -v "$(pwd)/outputs:/app/outputs" -v "$(pwd)/models:/app/models" webvox
	```

4. Run the jupyter notebook: [http://localhost:8888/main.ipynb](http://localhost:8888)

## Adding Dependencies

Add them to requirements.txt