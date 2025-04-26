import json
import time
from bs4 import BeautifulSoup
import ssl
import book_details
import isbn_scraper
import timeit


from urllib.request import urlopen
# Disable SSL verification
ssl._create_default_https_context = ssl._create_unverified_context

baseUrl = "https://www.goodreads.com"
preUserUrl = "/review/list/"
userUrl  = "174226910-halfdan-elvis?"
prePageUrl = "page="
pageNumber = "1"
postPageUrl = "&shelf=to-read"
# URL of the webpage to scrape
#global url = "https://www.goodreads.com/review/list/174226910-halfdan-elvis?page=1&shelf=to-read"
# https://www.goodreads.com/review/list/112401943-s-ren-jacobsen?ref=nav_mybooks&shelf=to-read
url = baseUrl+preUserUrl+userUrl+prePageUrl+pageNumber+postPageUrl


i = 0
books = []
print("scraping GoodReads...")
start_time = time.perf_counter()

while True:
    page = urlopen(url)
    response = page.read().decode("utf-8")
    soup = BeautifulSoup(response, 'html.parser')

    fields = soup.find_all('td', class_='field title')
    if not fields: break    
    for page in fields:
        i += 1
        x = page.find('div', 'value')
        title = x.a.text
        title = ' '.join(title.strip().split())
        grUrl = baseUrl+x.a['href']
        book = book_details.Book(title=title, url=grUrl)
        books.append(book)
    pageNumber = str((int(pageNumber)) + 1)
    url = baseUrl+preUserUrl+userUrl+prePageUrl+pageNumber+postPageUrl


print(f"took: {time.perf_counter()-start_time} seconds")
print()

print("Finding ISBN numbers...")
start_time = time.perf_counter()

book_count = len(books)
for idx, book in enumerate(books):
    print(f'{idx}/{book_count} Getting ISB for {book.title}')
    book.setISBN(isbn_scraper.get_isbn_new(book))


print(f"took: {time.perf_counter()-start_time} seconds")
print()

print("Generating .JSON file...")
start_time = time.perf_counter()

data = [book.to_dict() for book in books]

print(f"took: {time.perf_counter()-start_time} seconds")

with open("booksJSON.json", "w") as booksJSON:
    json.dump(data, booksJSON, indent=2, ensure_ascii=True)


