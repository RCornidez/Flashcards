# flashcardModel.py

class Flashcard:
    def __init__(self, title, content, tags=None):
        self.title = title
        self.content = content
        self.tags = tags if tags is not None else []

    # method for converting to a dictionary before storing to MongoDB
    def to_dict(self):
        return {
            "title": self.title,
            "content": self.content,
            "tags": self.tags
        }
