class Book:
    def __init__(self, title: str, url: str, ISBN=""):
        self.title = title
        self.ISBN = ISBN
        self.url = url

    def setISBN(self, ISBN: str):
        self.ISBN = ISBN