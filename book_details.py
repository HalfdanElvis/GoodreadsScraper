class Book:
    def __init__(self, title: str, url: str, ISBN="", ASIN=""):
        self.title = title
        self.ISBN = ISBN
        self.url = url
        self.ASIN = ASIN

    def setISBN(self, ISBN: str):
        self.ISBN = ISBN
    
    def setASIN(self, ASIN: str):
        self.ASIN = ASIN

    def __str__(self):
        return f"Title: {self.title}, ISBN: {self.ISBN}, URL: {self.url}"


    def to_dict(self):
        return {"ISBN": self.ISBN, "Title": self.title, "URL": self.url}