import requests
from bs4 import BeautifulSoup

class Content:
	def __init__(self, url, content_type):
		self.url = url
		self.content_type = content_type
		self.text = None

	def scrape(self):
		response = requests.get(self.url)
		if response.status_code == 200:
			soup = BeautifulSoup(response.text, 'html.parser')
			if self.content_type == "blog":
				self.text = self._scrape_blog(soup)
		else:
			print(f"Failed to fetch the page. Status code: {response.status_code}")
			return None

	def _scrape_blog(self, soup):
		return soup.get_text(separator=' ', strip=True) if soup else None