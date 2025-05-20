from dataclasses import dataclass
from extensions import db

@dataclass
class Book(db.Model):
    book_id: int
    title: str
    publisher_id: int
    cover_image: str
    author_id: int
    synopsis: str

    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    publisher_id = db.Column(db.Integer, db.ForeignKey('publisher.publisher_id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.author_id'), nullable=False)
    cover_image = db.Column(db.Text)
    synopsis = db.Column(db.Text)

    # Relationships
    publisher = db.relationship('Publisher', backref=db.backref('publisher_books', lazy=True))
    author = db.relationship('Author', backref=db.backref('author_books', lazy=True))
    book_user_relations = db.relationship('UserBook', back_populates='book_relation')
    genres = db.relationship('Genre', secondary='book_genre', back_populates='books')
    
    def __repr__(self):
        return f'<Book {self.title}>'
