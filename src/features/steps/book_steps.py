import requests
from behave import given, when, then


BASE_URL = "http://localhost:5000"

@given('que a API está rodando')
def step_impl(context):
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    # Criar livro para o teste de update
    payload = {
        "title": "Clean Code",
        "publisher_id": 1,
        "cover_image": "http://example.com/capa.jpg",
        "author_id": 1,
        "synopsis": "Sinopse inicial"
    }
    resp = requests.post(f"{BASE_URL}/books", json=payload)
    assert resp.status_code == 201
    context.book_id = resp.json().get("book", {}).get("book_id")


@when('eu cadastro um livro com título "{title}", publisher_id "{publisher_id}", cover_image "{cover_image}", author_id "{author_id}", e sinopse "{synopsis}"')
def step_impl(context, title, publisher_id, cover_image, author_id, synopsis):
    payload = {
        "title": title,
        "publisher_id": int(publisher_id),
        "cover_image": cover_image,
        "author_id": int(author_id),
        "synopsis": synopsis
    }
    response = requests.post(f"{BASE_URL}/books", json=payload)
    context.response = response
    context.book_id = response.json().get("book", {}).get("book_id")

@when('eu atualizo a sinopse do livro para "{new_synopsis}"')
def step_impl(context, new_synopsis):
    # Usa o book_id do contexto, que precisa existir (ex: criado no Given)
    book_id = context.book_id
    payload = {"synopsis": new_synopsis}
    response = requests.put(f"{BASE_URL}/books/{book_id}", json=payload)
    context.response = response

@then('o livro deve ser cadastrado com sucesso com status 201')
def step_impl(context):
    assert context.response.status_code == 201

@then('o livro deve ser atualizado com sucesso com status 200')
def step_impl(context):
    assert context.response.status_code == 200

@then('a sinopse do livro deve ser "{expected_synopsis}"')
def step_impl(context, expected_synopsis):
    data = context.response.json()
    assert data["book"]["synopsis"] == expected_synopsis


@when('eu busco o livro com id "{book_id}"')
def step_impl(context, book_id):
    response = requests.get(f"{BASE_URL}/books/{book_id}")
    context.response = response

@then('o livro deve ser retornado com status 200')
def step_impl(context):
    assert context.response.status_code == 200

@then('o título do livro deve ser "{expected_title}"')
def step_impl(context, expected_title):
    data = context.response.json()
    print("Resposta da API:", data)
    assert "book" in data
    assert data["book"]["title"] == expected_title

@when('eu deleto o livro com id "{book_id}"')
def step_impl(context, book_id):
    response = requests.delete(f"{BASE_URL}/books/{book_id}")
    context.response = response

@then('o livro deve ser deletado com sucesso com status 204')
def step_impl(context):
    assert context.response.status_code == 204

@given('que um livro com título "{title}" está cadastrado')
def step_impl(context, title):
    payload = {
        "title": title,
        "publisher_id": 1,
        "cover_image": "http://example.com/capa.jpg",
        "author_id": 1,
        "synopsis": "Sinopse para teste"
    }
    response = requests.post(f"{BASE_URL}/books", json=payload)
    print("Resposta cadastro livro:", response.status_code, response.json())
    assert response.status_code == 201
    context.book_id = response.json().get("book", {}).get("book_id")

@when('eu busco livros com título contendo "{title_part}"')
def step_impl(context, title_part):
    response = requests.get(f"{BASE_URL}/books/search", params={"title": title_part})
    context.response = response

@then('a API deve retornar uma lista de livros com status 200')
def step_impl(context):
    assert context.response.status_code == 200
    data = context.response.json()
    assert "books" in data

@then('pelo menos um livro deve conter "{title_part}" no título')
def step_impl(context, title_part):
    data = context.response.json()
    livros = data.get("books", [])
    print("Livros retornados:", livros)
    if not livros:
        print("Resposta completa:", context.response.text)
    print("Livros retornados:", livros)
    assert any(title_part.lower() in livro["title"].lower() for livro in livros)
