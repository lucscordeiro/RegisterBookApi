from dataclasses import dataclass
from extensions import db

@dataclass
class WeekRecomendation(db.Model):
    recomendation_id: int
    book_id: int
    title: str
    citation: str

    recomendation_id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.book_id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    citation = db.Column(db.String(255), nullable=True)  

    # Relationship
    book = db.relationship('Book', backref=db.backref('week_recommendations', lazy=True))

    def __repr__(self):
        return f'<WeekRecomendation {self.title} for BookID={self.book_id}>'
