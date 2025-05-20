from dataclasses import dataclass
from extensions import db

@dataclass
class Publisher(db.Model):
    publisher_id: int
    name: str

    publisher_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
        return f'<Publisher {self.name}>'
