import pytest
from models import User
from services.user_service import UserService
from extensions import db
from app import create_app

@pytest.fixture(scope='module')
def test_app():
    app = create_app()
    app.testing = True
    with app.app_context():
        yield app

@pytest.fixture(scope='function')
def setup_database(test_app):
    # Limpa e cria as tabelas para cada teste
    db.drop_all()
    db.create_all()
    yield
    db.session.remove()
    db.drop_all()

def test_create_user_success(setup_database):
    user = UserService.create_user(
        first_name="Lucas",
        last_name="Cordeiro",
        nickname="lucas123",
        cpf="12345678900",
        phone_number="11999999999",
        password="senha123"
    )
    assert user is not None
    assert user.nickname == "lucas123"
    assert user.cpf == "12345678900"

def test_create_user_missing_fields(setup_database):
    with pytest.raises(ValueError):
        UserService.create_user(
            first_name="Lucas",
            last_name="",
            nickname="",
            cpf="",
            phone_number="",
            password=""
        )

def test_create_user_first_name_empty(setup_database):
    with pytest.raises(ValueError):
        UserService.create_user(
            first_name="",
            last_name="Sobrenome",
            nickname="apelido",
            cpf="12345678900",
            phone_number="11999999999",
            password="senha123"
        )

def test_create_user_last_name_empty(setup_database):
    with pytest.raises(ValueError):
        UserService.create_user(
            first_name="Nome",
            last_name="",
            nickname="apelido",
            cpf="12345678900",
            phone_number="11999999999",
            password="senha123"
        )

def test_create_user_nickname_empty(setup_database):
    with pytest.raises(ValueError):
        UserService.create_user(
            first_name="Nome",
            last_name="Sobrenome",
            nickname="",
            cpf="12345678900",
            phone_number="11999999999",
            password="senha123"
        )

def test_create_user_duplicate_cpf_or_nickname(setup_database):
    UserService.create_user(
        first_name="Lucas",
        last_name="Cordeiro",
        nickname="lucas123",
        cpf="12345678900",
        phone_number="11999999999",
        password="senha123"
    )
    # Tentar criar com mesmo CPF ou nickname
    user = UserService.create_user(
        first_name="Outro",
        last_name="Usuário",
        nickname="lucas123",
        cpf="12345678900",
        phone_number="11988888888",
        password="senha456"
    )
    assert user is None

def test_get_user_by_id(setup_database):
    user = UserService.create_user(
        first_name="Lucas",
        last_name="Cordeiro",
        nickname="lucas123",
        cpf="12345678900",
        phone_number="11999999999",
        password="senha123"
    )
    found = UserService.get_user_by_id(user.user_id)
    assert found is not None
    # assert found.user_id == user.user_id


def test_delete_user(setup_database):
    user = UserService.create_user(
        first_name="Lucas",
        last_name="Cordeiro",
        nickname="lucas123",
        cpf="12345678900",
        phone_number="11999999999",
        password="senha123"
    )
    result = UserService.delete_user(user.user_id)
    assert result is True
    assert UserService.get_user_by_id(user.user_id) is None

def test_authenticate_user_success(setup_database):
    UserService.create_user(
        first_name="Lucas",
        last_name="Cordeiro",
        nickname="lucas123",
        cpf="12345678900",
        phone_number="11999999999",
        password="senha123"
    )
    user = UserService.authenticate_user("lucas123", "senha123")
    assert user is not None
    user = UserService.authenticate_user("12345678900", "senha123")
    assert user is not None

def test_authenticate_user_fail(setup_database):
    UserService.create_user(
        first_name="Lucas",
        last_name="Cordeiro",
        nickname="lucas123",
        cpf="12345678900",
        phone_number="11999999999",
        password="senha123"
    )
    user = UserService.authenticate_user("lucas123", "senhaerrada")
    assert user is None
    user = UserService.authenticate_user("cpf_invalido", "senha123")
    assert user is None
