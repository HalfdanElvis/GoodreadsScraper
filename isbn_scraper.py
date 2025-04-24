from bs4 import BeautifulSoup
import ssl
from urllib.request import urlopen
# Disable SSL verification
ssl._create_default_https_context = ssl._create_unverified_context
from book_details import Book
import json

def get_isbn(book: Book):
    page = urlopen(book.url)
    response = page.read().decode("utf-8")
    soup = BeautifulSoup(response, 'html.parser')
    scripts = soup.find_all("script", type="application/ld+json")
    for script in scripts:
        try:
            data = json.loads(script.string)
            # If it's a list of items, loop through
            if isinstance(data, list):
                for item in data:
                    if item.get("@type") == "Book" and "isbn" in item:
                        return item["isbn"]
            elif data.get("@type") == "Book" and "isbn" in data:
                return data["isbn"]
        except (json.JSONDecodeError, TypeError):
            continue

    return None  # If not found





