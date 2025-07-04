from flask import Flask, request, make_response
from flask_restx import Api
from extensions import db
from config.config import Config
from controllers import (
    author_controller, book_controller, genre_controller,
    publisher_controller, user_book_controller, user_controller,
    week_recomendation_controller, health_controller
)
from services.user_service import UserService
from flask_cors import CORS

from models import Author, Publisher, Genre, Book

user = UserService()

def seed_database():
    if not Author.query.first():
        author = Author(first_name="John", last_name="Doe", bio="Autor de testes")
        publisher = Publisher(name="Editora Teste")
        genre = Genre(name="Ficção")

        book = Book(
            title="Livro de Teste",
            publisher=publisher,
            author=author,
            cover_image="http://example.com/img.jpg",
            synopsis="Um livro fictício para testes."
        )
        book.genres.append(genre)

        db.session.add_all([author, publisher, genre, book])
        db.session.commit()
        print("Banco populado com dados de teste.")

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)
    db.init_app(app)

    api = Api(
        app,
        title="RegisterBook API",
        version="1.0",
        description="A API to manage book registration",
        doc='/docs'
    )

    api.add_namespace(user_controller.api, path='/users')
    api.add_namespace(book_controller.api, path='/books')
    api.add_namespace(publisher_controller.api, path='/publishers')
    api.add_namespace(author_controller.api, path='/authors')
    api.add_namespace(genre_controller.api, path='/genres')
    api.add_namespace(user_book_controller.api, path='/userbooks')
    api.add_namespace(week_recomendation_controller.api, path='/weekrecomendation')
    api.add_namespace(health_controller.api, path='/health')

    with app.app_context():
        db.create_all()
        seed_database()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
