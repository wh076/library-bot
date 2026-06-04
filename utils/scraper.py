import requests
from bs4 import BeautifulSoup
import random

def scrape_book_quote() -> dict:
    url = "https://quotes.toscrape.com/tag/books/"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return {"status": False, "error": "Failed to load page"}
        soup = BeautifulSoup(response.text, "html.parser")
        quotes_elements = soup.find_all("div", class_="quote")
        if not quotes_elements:
            return {"status": False, "error": "No quotes found"}
        chosen_quote = random.choice(quotes_elements)
        text = chosen_quote.find("span", class_="text").text
        author = chosen_quote.find("small", class_="author").text
        return {"status": True, "text": text, "author": author}
    except Exception as e:
        return {"status": False, "error": str(e)}