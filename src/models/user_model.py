from dataclasses import dataclass
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

@dataclass
class User(db.Model):
    user_id: int
    first_name: str
    last_name: str
    nickname: str
    cpf: str
    phone_number: str
    profile_picture: str
    quote: str

    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    nickname = db.Column(db.String(50), unique=True, nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    phone_number = db.Column(db.String(15))
    profile_picture = db.Column(db.String(500))
    _password = db.Column('password', db.String(255), nullable=False)
    quote = db.Column(db.Text)

    # Relationships
    user_books = db.relationship('UserBook', back_populates='user_relation')

    def set_password(self, password: str):
        self._password = generate_password_hash(password)
        

    def check_password(self, password: str) -> bool:
        return check_password_hash(self._password, password)

    def __repr__(self):
        return f'<User {self.first_name} {self.last_name}>'
