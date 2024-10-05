# Webvox

Get audio summarizes for any website, blog or paper

## Usage
1. Clone this repository:
	```
	git clone https://github.com/puravparab/webvox.git
	cd webvox
	```

### Notebooks
1. Follow the notebook [README](./notebooks) if you're setting up notebooks for the first time
2. Use shell script if you've completed inital setup
	```
	chmod +x run.sh
	./run.sh
	```

3. Run the jupyter notebook: [http://localhost:8888/main.ipynb](http://localhost:8888)

## Project Structure

```
webvox
├── notebooks/
|   ├── Dockerfile
|   ├── models/
|   ├── outputs/
│   └── main.ipynb
└── README.md
```