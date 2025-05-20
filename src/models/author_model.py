from dataclasses import dataclass
from extensions import db

@dataclass
class Author(db.Model):
    author_id: int
    first_name: str
    last_name: str
    bio: str

    author_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    bio = db.Column(db.Text)

    def __repr__(self):
        return f'<Author {self.first_name} {self.last_name}>'
