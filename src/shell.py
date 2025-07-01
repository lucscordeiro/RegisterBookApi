from  app import create_app
from extensions import db
from models import Book

app = create_app()

with app.app_context():
    books = Book.query.all()
    for book in books:
        print(f"{book.book_id} - {book.title}")
