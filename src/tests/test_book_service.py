import pytest
from app import create_app
from services.book_service import BookService

@pytest.fixture(scope='module')
def test_app():
    app = create_app()
    app.testing = True
    return app

def test_create_book_success(test_app):
    with test_app.app_context():
        book_service = BookService()
        book_data = {
            'title': 'Livro Teste',
            'publisher_id': 1,
            'cover_image': 'caminho/para/imagem.jpg',
            'author_id': 1,
            'synopsis': 'Resumo do livro para teste'
        }
        book = book_service.create_book(
            book_data['title'],
            book_data['publisher_id'],
            book_data['cover_image'],
            book_data['author_id'],
            book_data['synopsis']
        )
        assert book.title == 'Livro Teste'

