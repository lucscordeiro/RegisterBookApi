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

#CADASTRAR LIVRO
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

#CADASTRO INVÁLIDO DE LIVRO
@when('eu tento cadastrar um livro com dados inválidos faltando o campo "title"')
def step_impl(context):
    payload = {
        # "title": "deve estar ausente",
        "publisher_id": 1,
        "cover_image": "http://example.com/capa.jpg",
        "author_id": 1,
        "synopsis": "Livro sem título"
    }
    response = requests.post(f"{BASE_URL}/books", json=payload)
    context.response = response

@then('devo receber uma resposta de erro com status 400')
def step_impl(context):
    assert context.response.status_code == 400, f"Status esperado 400, retornado {context.response.status_code}"


#ATUALIZAR LIVRO
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

#ATUALIZAR LIVRO ID INEXISTENTE
@when('eu tento atualizar o livro com id "{book_id}" com a nova sinopse "{new_synopsis}"')
def step_impl(context, book_id, new_synopsis):
    payload = {"synopsis": new_synopsis}
    response = requests.put(f"{BASE_URL}/books/{book_id}", json=payload)
    context.response = response

#BUSCAR LIVRO POR ID
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

#BUSCAR LIVRO COM ID INEXISTENTE
@then('devo receber uma resposta de erro com status 404')
def step_impl(context):
    assert context.response.status_code == 404, f"Status esperado 404, retornado {context.response.status_code}"

#DELETAR LIVRO
@when('eu deleto o livro com id "{book_id}"')
def step_impl(context, book_id):
    response = requests.delete(f"{BASE_URL}/books/{book_id}")
    context.response = response

@then('o livro deve ser deletado com sucesso com status 204')
def step_impl(context):
    assert context.response.status_code == 204

