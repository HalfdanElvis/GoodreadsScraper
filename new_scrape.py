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

page = urlopen(url)
response = page.read().decode("utf-8")
soup = BeautifulSoup(response, 'html.parser')

fields = soup.find('tbody', id = 'booksBody')
books = fields.find_all('tr', class_='bookalike review')

for book in books:
    title = book.find('td', class_='field title').find('a')
    title = title.text.strip()
    print(title)
    
    isbn = book.find('td', class_='field isbn').find('div')
    isbn = isbn.text.strip()
    print(isbn)