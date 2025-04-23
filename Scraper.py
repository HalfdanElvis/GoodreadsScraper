import requests
from bs4 import BeautifulSoup
import ssl
import book_details
import isbn_scraper


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
url = baseUrl+preUserUrl+userUrl+prePageUrl+pageNumber+postPageUrl





i = 0
books = []
while True:
    page = urlopen(url)
    response = page.read().decode("utf-8")
    soup = BeautifulSoup(response, 'html.parser')
    scripts = soup.find_all('script')
    print(scripts)
    
    fields = soup.find_all('td', class_='field title')
    if not fields: break
    for page in fields:
        i += 1
        x = page.find('div', 'value')
        title = x.a.text
        grUrl = baseUrl+x.a['href']
        print("title: ", title)
        print("url: ", grUrl)
        book = book_details.Book(title=title, url=grUrl)
        books.append(book)
    pageNumber = str((int(pageNumber)) + 1)
    url = baseUrl+preUserUrl+userUrl+prePageUrl+pageNumber+postPageUrl

for book in books:
    test = book.setISBN(isbn_scraper.get_isbn(book))
    print("test: ",test)
    