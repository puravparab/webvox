FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
	build-essential \
	&& rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create models directory
RUN mkdir -p /app/models

# Copy the notebooks and the rest of the application code
COPY notebooks/ ./notebooks/

EXPOSE 8888

CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--notebook-dir=/app/notebooks", "--NotebookApp.token=''", "--NotebookApp.password=''"]