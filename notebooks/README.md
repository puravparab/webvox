# Webvox Notebooks
This directory consists of a notebook that demonstrates a audio summary pipeline that scrapes content from the web, summarizes it and creates an audio clip from the summary.

## Requirements
- python 3.11

## Setup
If MeloTTS is not in `models/` then run:
```
git pull --recurse-submodules
```

Activate poetry shell and install libraries:
```
poetry shell
```
```
poetry install
```

Run the following commands:
```
poetry run pip install -e ./models/MelosTTS
```
```
poetry run python -m unidic download
```

Run the jupyter notebook:
```
jupyter notebook
```