import json
from bs4 import BeautifulSoup
import book_details
import math
from urllib.request import urlopen

# Opstiller URL 
baseUrl = "https://www.goodreads.com"
preUserUrl = "/review/list/"
userUrl  = "112401943-s-ren-jacobsen?"
prePageUrl = "page="
pageNumber = "1"
postPageUrl = "&shelf=to-read"
url = baseUrl+preUserUrl+userUrl+prePageUrl+pageNumber+postPageUrl

# Åbner siden først, til at finde den totale mængde bøger.
page = urlopen(url)
response = page.read().decode("utf-8")
soup = BeautifulSoup(response, 'html.parser')
header = soup.find('div', id='header')
total_book_count = header.find('span', class_='greyText').text
total_book_count = total_book_count.replace('(', '').replace(')', '')
total_book_count = int(total_book_count)
print(f'Found {total_book_count} books on GoodReads bookshelf')

# Finder antallet af pages der skal scrapes.
page_count = math.ceil(total_book_count / 20)

books = []
# Scraper 20 bøger for hvert page
for page_idx in range(1, page_count + 1):
    print(f'Scraping page {page_idx}/{page_count}')
    url = baseUrl+preUserUrl+userUrl+prePageUrl+str(page_idx)+postPageUrl
    page = urlopen(url)
    response = page.read().decode("utf-8")
    soup = BeautifulSoup(response, 'html.parser')
    
    book_list = soup.find('tbody', id = 'booksBody')
    book_divs = book_list.find_all('tr', class_='bookalike review')

    for book in book_divs:
        title = book.find('td', class_='field title').find('a')
        url = 'goodreads.com' + title['href']
        title = title.text.strip().replace('\n', '')
        isbn = book.find('td', class_='field isbn').find('div')
        isbn = isbn.text.strip()
        books.append(book_details.Book(title=title, url=url, ISBN=isbn))

# Gemmer som JSON
filename = "new_booksJSON.json"
print(f'Writing {len(books)} books to {filename}')
if len(books) != total_book_count:
    print("Error: Total book count on GoodReads doesn't match amount of books saved.")

data = [book.to_dict() for book in books]
with open(filename, "w") as booksJSON:
    json.dump(data, booksJSON, indent=2, ensure_ascii=True)


