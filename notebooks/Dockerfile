FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
	build-essential \
	git \
	libsndfile1 \
	swig \
	&& rm -rf /var/lib/apt/lists/*

COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /app/outputs

# Install MeloTTS in the models folder
WORKDIR /app/models/MeloTTS
RUN pip install -e .
# Install unidic
RUN pip install unidic
# Download unidic dictionary
RUN python -m unidic download
# Install NLTK
RUN pip install nltk


WORKDIR /app

EXPOSE 8888

CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=''", "--NotebookApp.password=''"]