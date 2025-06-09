import requests
from behave import given, when, then

BASE_URL = "http://localhost:5000"

@given('que a API está rodando')
def step_impl(context):
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200

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

@then('o livro deve ser cadastrado com sucesso com status 201')
def step_impl(context):
    assert context.response.status_code == 201
    data = context.response.json()
    assert "book" in data
    assert "title" in data["book"]
    assert "publisher_id" in data["book"]
    assert "cover_image" in data["book"]
    assert "author_id" in data["book"]
    assert "synopsis" in data["book"]
