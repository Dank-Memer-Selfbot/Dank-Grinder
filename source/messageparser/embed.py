class Embed():
    def __init__(self, embed):
        self.author = Author(embed[0].author) if embed[0].author else None
        self.description = embed[0].description 
        self.title = embed[0].title 
        self.footer = embed[0].footer
        
        
class Author():
    def __init__(self, author):
        self.name = author.name if author.name else None
        self.url = author.url if author.url else None
        self.icon_url = author.icon_url if author.icon_url else None