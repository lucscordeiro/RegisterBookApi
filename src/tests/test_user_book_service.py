import pytest
from services.user_book_service import UserBookService
from services.user_service import UserService
from services.book_service import BookService
from extensions import db
from app import create_app
from models import UserBook

@pytest.fixture(scope='module')
def test_app():
    app = create_app()
    app.testing = True
    with app.app_context():
        yield app

@pytest.fixture(scope='function')
def setup_database(test_app):
    db.drop_all()
    db.create_all()
    yield
    db.session.remove()
    db.drop_all()

def test_add_user_book_success(setup_database):
    # Criar usuário para associar
    user = UserService.create_user(
        first_name="Lucas",
        last_name="Cordeiro",
        nickname="lucas123",
        cpf="12345678900",
        phone_number="11999999999",
        password="senha123"
    )
    # Criar livro para associar
    book = BookService.create_book(
        title="Livro Teste",
        publisher_id=1,
        author_id=1,
        synopsis="Sinopse teste",
        cover_image=None
    )
    assert user is not None
    assert book is not None
    
    # Testar adicionar livro ao usuário
    user_book = UserBookService.add_user_book(
        user_id=user.user_id,
        book_id=book.book_id,
        progress=25.0,
        rating=4.5,
        notes="Ótimo livro",
        favorite=True
    )
    
    assert user_book is not None
    assert user_book.user_id == user.user_id
    assert user_book.book_id == book.book_id
    assert user_book.progress == 25.0
    assert user_book.rating == 4.5
    assert user_book.notes == "Ótimo livro"
    assert user_book.favorite is True
