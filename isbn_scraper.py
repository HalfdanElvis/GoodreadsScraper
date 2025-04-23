from bs4 import BeautifulSoup
import ssl
from urllib.request import urlopen
# Disable SSL verification
ssl._create_default_https_context = ssl._create_unverified_context
from book_details import Book

def get_isbn(book: Book):
    page = urlopen(book.url)
    response = page.read().decode("utf-8")
    soup = BeautifulSoup(response, 'html.parser')
    print("Soup", soup)

    scripts = soup.find_all("script")
    print("Scripts ", scripts)
    
    return scripts


book = Book("test", "https://www.goodreads.com/book/show/9648068-the-first-days")
print(get_isbn(book))