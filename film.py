class Film:

    def __init__(self, title, release_year, id = None):
        self.id = id
        self.title = title
        self.release_year = release_year

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return f"Film({self.id}, {self.title}, {self.release_year})"
