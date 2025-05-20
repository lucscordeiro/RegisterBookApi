from dataclasses import dataclass
from extensions import db

@dataclass
class Genre(db.Model):
    genre_id: int
    name: str

    genre_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    books = db.relationship('Book', secondary='book_genre', back_populates='genres')

    def __repr__(self):
        return f'<Genre {self.name}>'
