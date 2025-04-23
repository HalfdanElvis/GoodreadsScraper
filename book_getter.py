from bs4 import BeautifulSoup
import ssl
from urllib.request import urlopen
import urllib.parse
# Disable SSL verification
ssl._create_default_https_context = ssl._create_unverified_context
from book_details import Book
import json

baseUrl = "https://z-library.sk"
stringSearchUrl = "?content_type=book&q="
preSearchUrl = "/s/"
searchUrl = ""
endSearchUrl = "?"
downloadUrl = ""

def search(url):
    page = urlopen(url)
    response = page.read().decode("utf-8")
    soup = BeautifulSoup(response, 'html.parser')

    fields = soup.find_all('div', class_='book-item')
    for page in fields:
        x = page.find('z-bookcard')
        href = x['href']
        return baseUrl+href

def download(url):
    page = urlopen(url)
    response = page.read().decode("utf-8")
    soup = BeautifulSoup(response, 'html.parser')

    fields = soup.find_all('div', class_='btn-group')
    for field in fields:
        x = field.find('a', class_='btn btn-default addDownloadedBook')
        if x and x.has_attr('href'):
            href = x['href']
            return baseUrl+href

with open('booksJSON.json') as booksjson:
    books = json.load(booksjson)

for book in books:
    if book["ISBN"]:
        url = baseUrl+preSearchUrl+book["ISBN"]+endSearchUrl
        url = search(url)
        print("ISBN: ", url)
        downloadUrl = download(url)
        print(downloadUrl)
        print()
    elif book["Title"]:
        encoded_title = urllib.parse.quote_plus(book["Title"])
        tempUrl = baseUrl+preSearchUrl+stringSearchUrl+encoded_title
        url = search(tempUrl)
        print("Title: ", url)
        downloadUrl = download(url)
        print(downloadUrl)
        print()
    



