from dataclasses import dataclass, field
from extensions import db

@dataclass
class UserBook(db.Model):
    user_book_id: int
    user_id: int
    book_id: int
    progress: float = field(init=False)
    rating: int = field(init=False)
    notes: str
    favorite: bool = field(default=False)  

    user_book_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.book_id'), nullable=False)
    _progress = db.Column('progress', db.Float)
    _rating = db.Column('rating', db.Integer)
    notes = db.Column(db.Text)
    favorite = db.Column(db.Boolean, default=False)  

    # Relacionamentos
    user_relation = db.relationship('User', back_populates='user_books')
    book_relation = db.relationship('Book', back_populates='book_user_relations')

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        if 1 <= value <= 10:
            self._rating = value
        else:
            raise ValueError('Rating must be between 1 and 10.')

    @property
    def progress(self):
        return self._progress

    @progress.setter
    def progress(self, value):
        if 0.0 <= value <= 100.0:
            self._progress = value
        else:
            raise ValueError('Progress must be between 0.0 and 100.0.')

    def __repr__(self):
        return f'<UserBook UserID={self.user_id} BookID={self.book_id}>'
