import pytest
from app import create_app
from extensions import db
from models import Publisher, Author, Genre
from services.book_service import BookService
from sqlalchemy.exc import IntegrityError
import uuid

@pytest.fixture(scope='function')
def test_app():
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def setup_entities(test_app):
    with test_app.app_context():
        unique_suffix = str(uuid.uuid4())[:8]
        publisher = Publisher(name=f'Editora Teste {unique_suffix}')
        author = Author(first_name='Autor', last_name='Teste')
        genre = Genre(name=f'Aventura {unique_suffix}')

        db.session.add_all([publisher, author, genre])
        db.session.commit()

        return {
            "publisher_id": publisher.publisher_id,
            "author_id": author.author_id,
            "genre_id": genre.genre_id
        }

def test_create_book_success(test_app, setup_entities):
    with test_app.app_context():
        book = BookService.create_book(
            title="Livro de Teste",
            publisher_id=setup_entities['publisher_id'],
            cover_image="imagem.jpg",
            author_id=setup_entities['author_id'],
            synopsis="Uma sinopse qualquer"
        )
        assert book is not None
        assert book.title == "Livro de Teste"

def test_create_book_title_none(test_app, setup_entities):
    client = test_app.test_client()
    response = client.post("/books/", json={
        "title": None,
        "publisher_id": setup_entities['publisher_id'],
        "cover_image": "imagem.jpg",
        "author_id": setup_entities['author_id'],
        "synopsis": "Uma sinopse qualquer"
    })

    assert response.status_code == 400
    assert "failed to create book" in response.get_data(as_text=True).lower()

def test_create_book_publisher_none(test_app, setup_entities):
    client = test_app.test_client()
    response = client.post("/books/", json={
        "title": "Livro de Teste",
        "publisher_id": None,
        "cover_image": "imagem.jpg",
        "author_id": setup_entities['author_id'],
        "synopsis": "Uma sinopse qualquer"
    })

    assert response.status_code == 400
    assert "failed to create book" in response.get_data(as_text=True).lower()

def test_create_book_author_none(test_app, setup_entities):
    client = test_app.test_client()
    response = client.post("/books/", json={
        "title": "Livro de Teste",
        "publisher_id": setup_entities['publisher_id'],
        "cover_image": "imagem.jpg",
        "author_id": None,
        "synopsis": "Uma sinopse qualquer"
    })

    assert response.status_code == 400
    assert "failed to create book" in response.get_data(as_text=True).lower()

def test_get_book_by_id(test_app, setup_entities):
    with test_app.app_context():
        book = BookService.create_book(
            title="Livro Buscado",
            publisher_id=setup_entities['publisher_id'],
            cover_image="imagem.jpg",
            author_id=setup_entities['author_id'],
            synopsis="Sinopse"
        )
        result = BookService.get_book_by_id(book.book_id)
        assert result is not None
        assert result.title == "Livro Buscado"

def test_get_book_by_nonexistent_id(test_app):
    with test_app.app_context():
        result = BookService.get_book_by_id(999)
        assert result is None

def test_get_book_by_negative_id(test_app):
    with test_app.app_context():
        result = BookService.get_book_by_id(-1)
        assert result is None

def test_update_book(test_app, setup_entities):
    with test_app.app_context():
        book = BookService.create_book(
            title="Livro Antigo",
            publisher_id=setup_entities['publisher_id'],
            cover_image="imagem.jpg",
            author_id=setup_entities['author_id'],
            synopsis="Velha sinopse"
        )
        updated = BookService.update_book(book.book_id, title="Livro Atualizado", synopsis="Nova sinopse")
        assert updated.title == "Livro Atualizado"
        assert updated.synopsis == "Nova sinopse"

def test_update_none_existent_book(test_app):
    with test_app.app_context():
        updated_book = BookService.update_book(999, title="Novo Livro")
        assert updated_book is None

def test_delete_book(test_app, setup_entities):
    with test_app.app_context():
        book = BookService.create_book(
            title="Livro Excluído",
            publisher_id=setup_entities['publisher_id'],
            cover_image="imagem.jpg",
            author_id=setup_entities['author_id'],
            synopsis="Para deletar"
        )
        result = BookService.delete_book(book.book_id)
        assert result is True
        assert BookService.get_book_by_id(book.book_id) is None

def test_delete_book_by_none_existent_id(test_app):
    with test_app.app_context():
        result = BookService.delete_book(999)
        assert result is None

def test_delete_book_by_negative_id(test_app):
    with test_app.app_context():
        result = BookService.delete_book(-1)
        assert result is None

def test_add_genre_to_book(test_app, setup_entities):
    with test_app.app_context():
        book = BookService.create_book(
            title="Livro com Gênero",
            publisher_id=setup_entities['publisher_id'],
            cover_image="imagem.jpg",
            author_id=setup_entities['author_id'],
            synopsis="Com gênero"
        )
        result = BookService.add_genre_to_book(book.book_id, setup_entities['genre_id'])
        assert result is True

def test_get_books_by_title(test_app, setup_entities):
    with test_app.app_context():
        BookService.create_book(
            title="Livro Python",
            publisher_id=setup_entities['publisher_id'],
            cover_image="img.jpg",
            author_id=setup_entities['author_id'],
            synopsis="Aprenda Python"
        )
        books = BookService.get_books_by_title("python")
        assert books
        assert books[0].title == "Livro Python"
