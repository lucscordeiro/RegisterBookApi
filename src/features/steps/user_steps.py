import requests
from behave import given, when, then

BASE_URL = "http://localhost:5000"

@given('que o serviço de usuários está disponível')
def step_impl(context):
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200

@when('eu envio os dados do novo usuário:')
def step_impl(context):
    payload = {}
    for row in context.table:
        payload[row[0]] = row[1]
    context.payload = payload

    response = requests.post(f"{BASE_URL}/users", json=context.payload)
    context.response = response

@then('o usuário deve ser criado com sucesso com status 201')
def step_impl(context):
    assert context.response.status_code == 201, f"Esperado 201, obtido {context.response.status_code}"

@then('o retorno deve conter o nickname "{nickname}"')
def step_impl(context, nickname):
    data = context.response.json()
    assert "user" in data
    assert data["user"]["nickname"] == nickname

@then('devo receber uma resposta de erro com status 400')
def step_impl(context):
    assert context.response.status_code == 400, f"Esperado 400, obtido {context.response.status_code}"
