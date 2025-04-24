import re
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
contentTypeBook = "/?content_type=book"

def search(url):
    page = urlopen(url)
    response = page.read().decode("utf-8")
    soup = BeautifulSoup(response, 'html.parser')

    # Try to get href from z-bookcard
    fields = soup.find_all('div', class_='book-item')
    for field in fields:
        x = field.find('z-bookcard')
        if x and x.has_attr('href'):
            href = x['href']
            print("Found href in z-bookcard:", href)
            return baseUrl + href

    # If not found, try alternative: a.title in book-info
    fields = soup.find_all('div', class_='book-info')
    for field in fields:
        x = field.find('a', class_='title')
        if x and x.has_attr('href'):
            href = x['href']
            print("Fallback href from book-info:", href)
            return baseUrl + href

    # If nothing found
    print("No book href found.")
    return None

def download(url):
    page = urlopen(url)
    response = page.read().decode("utf-8")
    soup = BeautifulSoup(response, 'html.parser')
    href = None

    # Try to get href from btn-default
    fields = soup.find_all('div', class_='btn-group')
    for field in fields:
        x = field.find('a', class_='btn btn-default addDownloadedBook')
        if x and x.has_attr('href'):
            href = x['href']
            return baseUrl + href
    
    # Try to get href from btn-primary
    for field in fields:
        x = field.find('a', class_='btn btn-primary addDownloadedBook')
        if x and x.has_attr('href'):
            href = x['href']
            return baseUrl + href
    
    # If nothing found
    print("No download href found.")
    return None
    






with open('booksJSON.json') as booksjson:
    books = json.load(booksjson)

for book in books:
    print(book["Title"], ":")
    
    if book["ISBN"]:
        print("Searching via ISBN...")
        tempUrl = baseUrl+preSearchUrl+book["ISBN"]+endSearchUrl
        url = search(tempUrl)

    elif book["Title"] or url == None:
        print("Searching via Title...")
        encoded_title = urllib.parse.quote_plus(book["Title"])
        tempUrl = baseUrl+preSearchUrl+stringSearchUrl+encoded_title
        url = search(tempUrl)
        if url == None:
            # DOESNT WORK YET
            cleaned_title = re.sub(r'[^A-Za-z0-9 ]+', '', book["Title"])
            cleaned_title = re.sub(r'[ ]+', '%20', cleaned_title)
            tempUrl = baseUrl+preSearchUrl+cleaned_title+contentTypeBook
            url = search(tempUrl)
    
    if url and download(url) == None:
        cleaned_title = book["Title"].split('(')[0].strip()
        tempUrl = url = baseUrl+preSearchUrl+cleaned_title+endSearchUrl
        url = search(tempUrl)

    if url:
        downloadUrl = download(url)
        print("download link: ", downloadUrl)
    else:
        print("Book couldn't be found")
    print()



