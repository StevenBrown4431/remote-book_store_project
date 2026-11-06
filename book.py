class Book:

    def __init__(self, title, author, synopsis, rating, image_url, notes, id = None):
        self.id = id
        self.title = title
        self.author = author
        self.synopsis = synopsis
        self.rating = rating
        self.image_url = image_url
        self.notes = notes

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return f"Book({self.id}, {self.title}, {self.author}, {self.synopsis}, {self.rating}, {self.image_url}, {self.notes})"