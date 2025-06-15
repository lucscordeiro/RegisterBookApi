import requests
from behave import given, when, then

BASE_URL = "http://localhost:5000"

@given('que a API está rodando para user book')
def step_impl(context):
    # Cria um usuário
    user_payload = {
        "first_name": "Lucas",
        "last_name": "Cordeiro",
        "nickname": "lucasdev",
        "cpf": "12345678900",
        "phone_number": "11999999999",
        "profile_picture": "https://exemplo.com/foto.png",
        "password": "senha123",
        "quote": "Aprendizado constante é a chave."
    }
    user_resp = requests.post(f"{BASE_URL}/users", json=user_payload)
    assert user_resp.status_code == 201, f"Erro ao criar usuário: {user_resp.text}"
    context.user_id = user_resp.json()["user"]["user_id"]

    # Cria um author
    author_payload = {
        "first_name": "Robert",
        "last_name": "Martin",
        "bio": "Autor renomado na área de engenharia de software"
    }
    author_resp = requests.post(f"{BASE_URL}/authors", json=author_payload)
    assert author_resp.status_code == 201, f"Erro ao criar author: {author_resp.text}"
    context.author_id = author_resp.json()["author"]["author_id"]

    # Cria um publisher (editora)
    publisher_payload = {
        "name": "Alta Books"
    }
    publisher_resp = requests.post(f"{BASE_URL}/publishers", json=publisher_payload)
    assert publisher_resp.status_code == 201, f"Erro ao criar publisher: {publisher_resp.text}"
    context.publisher_id = publisher_resp.json()["publisher"]["publisher_id"]

    # Cria um livro com os ids de author e publisher
    book_payload = {
        "title": "Clean Code",
        "publisher_id": context.publisher_id,
        "author_id": context.author_id,
        "cover_image": "https://exemplo.com/clean_code.jpg",
        "synopsis": "Livro sobre boas práticas de programação."
    }
    book_resp = requests.post(f"{BASE_URL}/books", json=book_payload)
    assert book_resp.status_code == 201, f"Erro ao criar livro: {book_resp.text}"
    context.book_id = book_resp.json()["book"]["book_id"]

#ADICIONAR LIVRO A LISTA DO USUÁRIO
@when('eu adiciono o livro com id "{book_id}" para o usuário com id "{user_id}" com progresso "{progress}", nota "{rating}", anotações "{notes}" e favorito "{favorite}"')
def step_impl(context, book_id, user_id, progress, rating, notes, favorite):
    payload = {
        "user_id": int(user_id),
        "book_id": int(book_id),
        "progress": float(progress),
        "rating": int(rating),
        "notes": notes,
        "favorite": favorite.lower() == 'true'
    }
    response = requests.post(f"{BASE_URL}/userbooks", json=payload)
    context.response = response

@then('o livro deve ser adicionado com sucesso com status 201')
def step_impl(context):
    print("Status Code:", context.response.status_code)
    try:
        response_json = context.response.json()
        print("Response JSON:", response_json)
    except Exception as e:
        print("Erro ao decodificar JSON:", str(e))
        response_json = {}
    assert context.response.status_code == 201, f"Resposta inesperada: {context.response.status_code}, body: {context.response.text}"
    context.response_json = response_json

@then('o progresso do livro deve ser "{expected_progress}"')
def step_impl(context, expected_progress):
    data = context.response_json
    assert "user_book" in data, f"'user_book' não encontrado na resposta: {data}"
    actual_progress = str(data["user_book"]["progress"])
    assert actual_progress == expected_progress, f"Esperado {expected_progress}, mas veio {actual_progress}"
