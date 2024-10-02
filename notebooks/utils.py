import os
import requests
import tiktoken
from bs4 import BeautifulSoup
from huggingface_hub import login, hf_hub_download
from llama_cpp import Llama
# from transformers import AutoTokenizer
# from ctransformers import AutoModelForCausalLM

from dotenv import load_dotenv
load_dotenv(override=True)

class Content:
	def __init__(self, url, content_type):
		"""
		Initialize a Content object.

		Args:
			url (str): The URL of the content to be scraped.
			content_type (str): The type of content (e.g., "blog").
		"""
		self.url = url
		self.content_type = content_type
		self.text = None
		self.token_count = 0
		self.tokenizer = None
		self.summary = {
			"model": None,
			"text": None,
			"token_count": 0,
			"tokenizer": None
		}

	def scrape(self):
		"""
		Scrape the content from the URL.

		Returns:
			None: The scraped content is stored in self.text.
		"""
		response = requests.get(self.url)
		if response.status_code == 200:
			soup = BeautifulSoup(response.text, 'html.parser')
			if self.content_type == "blog":
				self.text = self._scrape_blog(soup)
			self.tokenize()
		else:
			print(f"Failed to fetch the page. Status code: {response.status_code}")
			return None

	def _scrape_blog(self, soup):
		"""
		Extract text content from a blog page.

		Args:
			soup (BeautifulSoup): Parsed HTML content.

		Returns:
			str: Extracted text content.
		"""
		return soup.get_text(separator=' ', strip=True) if soup else None

	def tokenize(self, default=True, tokenizer=None):
		"""
		Tokenize the scraped text content.

		Args:
			default (bool): If True, use tiktoken for tokenization.
			tokenizer: Custom tokenizer object (if default is False).

		Raises:
			ValueError: If self.text is None or tokenizer is None when required.
		"""
		# Use tiktoken
		if default:
			encoding = tiktoken.get_encoding("cl100k_base")  # Specify the encoding name
			if self.text:
				self.token_count = len(encoding.encode(self.text))
			else:
				raise ValueError("self.text cannot be None")
		
		# Use model specific tokenizer
		elif tokenizer:
			self.tokenizer = tokenizer
			if self.text:
				tokens = self.tokenizer.encode(self.text)
				self.token_count = len(tokens)
			else:
				raise ValueError("self.text cannot be None")
		else:
			raise ValueError("tokenizer cannot be None when default is False")

	def add_summary(self, model, summary, tokenizer, token_count):
		"""
		Add a summary of the content.

		Args:
			model (str): The model used for summarization.
			summary (str): The generated summary text.
			tokenizer: The tokenizer used for the summary.
			token_count (int): The token count of the summary.
		"""
		self.summary["model"] = model
		self.summary["text"] = summary
		self.summary["tokenizer"] = tokenizer
		self.summary["token_count"] = token_count


def login_hf():
	"""
	Log into Hugging Face to download models.

	Raises:
		ValueError: If HF_TOKEN is not found in the environment variables.

	Note:
		Must HF_TOKEN is present in .env file.
	"""
	hf_token = os.getenv('HF_TOKEN')
	if not hf_token:
		raise ValueError("HF_TOKEN not found in .env")
	login(token=hf_token)


def load_model(repo_id, filename, model_dir="../models"):
	"""
	Load the Llama model using the official API, storing it in ../models/.

	Args:
		repo_id (str): Repository ID on Hugging Face (e.g., "lmstudio-community/Llama-3.2-3B-Instruct-GGUF").
		filename (str): Specific filename of the model (e.g., "Llama-3.2-3B-Instruct-Q3_K_L.gguf").
		model_dir (str): Directory to store the model files. Defaults to "models/".

	Returns:
		Llama: Loaded model
	"""
	os.makedirs(model_dir, exist_ok=True)
	full_path = os.path.join(model_dir, filename)
	
	if os.path.exists(model_dir):
		print(f"Loading existing model: `{filename}` from models/")
	else:
		print(f"Downloading model: `{filename}` to models/")

	return Llama.from_pretrained(
		repo_id=repo_id,
		filename=filename,
		cache_dir=model_dir,
		verbose=False
	)

# def load_model(model_name, model_type="llama"):
# 	"""
# 	Load the model and tokenizer. If the model doesn't exist locally, download it from Hugging Face.

# 	Args:
# 		model_name (str): Name of the model on Hugging Face (e.g., "lmstudio-community/Llama-3.2-3B-Instruct-GGUF").
# 		model_type (str): Type of the model (default is "llama").

# 	Returns:
# 		tuple: (model, tokenizer)
# 	"""
# 	# Define the local directory to store models
# 	current_dir = os.path.dirname(os.path.abspath(__file__))
# 	local_model_dir = os.path.join(current_dir, "models")
# 	if not os.path.exists(local_model_dir):
# 		os.makedirs(local_model_dir)

# 	# Extract the filename from the model_name
# 	model_filename = model_name.split("/")[-1] + ".gguf"
# 	local_model_path = os.path.join(local_model_dir, model_filename)

# 	# Check if the model exists locally
# 	if not os.path.exists(local_model_path):
# 		print(f"Model not found locally. Downloading from Hugging Face: {model_name}")
# 		try:
# 			# Download the model from Hugging Face
# 			hf_hub_download(repo_id=model_name, filename=model_filename, local_dir=local_model_dir)
# 		except Exception as e:
# 			print(f"Error downloading the model: {e}")
# 			return None, None

# 	# Load the model
# 	try:
# 		model = AutoModelForCausalLM.from_pretrained(local_model_path, model_type=model_type)
# 	except Exception as e:
# 		print(f"Error loading the model: {e}")
# 		return None, None

# 	# Load the tokenizer
# 	try:
# 		tokenizer = AutoTokenizer.from_pretrained(model_name)
# 	except Exception as e:
# 		print(f"Error loading the tokenizer: {e}")
# 		return model, None

# 	return model, tokenizer