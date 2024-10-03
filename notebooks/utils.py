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


def load_model(repo_id, filename, model_dir="../models", verbose=False, context_length=3000):
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
		repo_id=repo_id,           # Hugging Face repository ID
		filename=filename,         # Specific model file to load
		cache_dir=model_dir,       # Directory to store the model
		verbose=verbose,           # Enable detailed output during loading
		n_ctx=context_length,      # Set context window size (adjust as needed)
		# n_gpu_layers=-1,         # Use all available GPU layers
		# use_metal=True,          # Enable Metal acceleration for M-series chips
		# use_mlock=True,          # Lock memory to prevent swapping
		# use_mmap=True,           # Use memory mapping for faster loading
		# n_threads=os.cpu_count() # Use all available CPU cores
	)