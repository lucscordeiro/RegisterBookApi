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
    user = UserService.create_user(
        first_name="Lucas",
        last_name="Cordeiro",
        nickname="lucas123",
        cpf="12345678900",
        phone_number="11999999999",
        password="senha123"
    )
    book = BookService.create_book(
        title="Livro Teste",
        publisher_id=1,
        author_id=1,
        synopsis="Sinopse teste",
        cover_image=None
    )
    assert user is not None
    assert book is not None

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

def test_add_user_book_invalid_user_id(setup_database):
    book = BookService.create_book(
        title="Livro Teste",
        publisher_id=1,
        author_id=1,
        synopsis="Sinopse teste",
        cover_image=None
    )
    assert book is not None

    user_book = UserBookService.add_user_book(
        user_id=999,  # usuário inexistente
        book_id=book.book_id,
        progress=20.0,
        rating=3.0,
        notes="Teste usuário inválido",
        favorite=False
    )
    assert user_book is not None
    assert user_book.user_id == 999
    assert user_book.book_id == book.book_id

def test_add_user_book_invalid_book_id(setup_database):
    user = UserService.create_user(
        first_name="Lucas",
        last_name="Cordeiro",
        nickname="lucas123",
        cpf="12345678900",
        phone_number="11999999999",
        password="senha123"
    )
    assert user is not None

    user_book = UserBookService.add_user_book(
        user_id=user.user_id,
        book_id=999,  # livro inexistente
        progress=20.0,
        rating=3.0,
        notes="Teste livro inválido",
        favorite=False
    )
    assert user_book is not None
    assert user_book.user_id == user.user_id
    assert user_book.book_id == 999

def test_add_user_book_progress_above_100(setup_database):
    user = UserService.create_user(
        first_name="Lucas", last_name="Cordeiro", nickname="lucas123",
        cpf="12345678900", phone_number="11999999999", password="senha123"
    )
    book = BookService.create_book(
        title="Livro Teste", publisher_id=1, author_id=1,
        synopsis="Sinopse teste", cover_image=None
    )
    assert user is not None and book is not None

    with pytest.raises(ValueError) as excinfo:
        UserBookService.add_user_book(
            user_id=user.user_id,
            book_id=book.book_id,
            progress=150.0,  # inválido
            rating=4.0,
            notes="Progresso inválido",
            favorite=False
        )
    assert "Progress must be between" in str(excinfo.value)

# def test_add_user_book_rating_above_5(setup_database):
#     user = UserService.create_user(
#         first_name="Lucas", last_name="Cordeiro", nickname="lucas123",
#         cpf="12345678900", phone_number="11999999999", password="senha123"
#     )
#     book = BookService.create_book(
#         title="Livro Teste", publisher_id=1, author_id=1,
#         synopsis="Sinopse teste", cover_image=None
#     )
#     assert user is not None and book is not None

#     with pytest.raises(ValueError) as excinfo:
#         UserBookService.add_user_book(
#             user_id=user.user_id,
#             book_id=book.book_id,
#             progress=50.0,
#             rating=6.0,  # inválido
#             notes="Nota inválida",
#             favorite=False
#         )
#     assert "Rating must be between" in str(excinfo.value)

def test_add_user_book_favorite_non_boolean(setup_database):
    user = UserService.create_user(
        first_name="Lucas", last_name="Cordeiro", nickname="lucas123",
        cpf="12345678900", phone_number="11999999999", password="senha123"
    )
    book = BookService.create_book(
        title="Livro Teste", publisher_id=1, author_id=1,
        synopsis="Sinopse teste", cover_image=None
    )
    assert user is not None and book is not None

    user_book = UserBookService.add_user_book(
        user_id=user.user_id,
        book_id=book.book_id,
        progress=30.0,
        rating=4.0,
        notes="Favorite inválido",
        favorite="sim"  # valor inválido
    )
    # Pode ser None ou pode lançar exceção, dependendo do banco.
    # Aqui só testamos que o retorno é None (não criado)
    assert user_book is None
