Feature: Criar usuário

  Scenario: Usuário é criado com sucesso
    Given que o serviço de usuários está disponível
    When eu envio os dados do novo usuário:
      | first_name      | Lucas         |
      | last_name       | Cordeiro      |
      | nickname        | lucas123      |
      | cpf             | 12345678900   |
      | phone_number    | 11999999999   |
      | password        | senha123      |
    Then o usuário deve ser criado com sucesso com status 201
    And o retorno deve conter o nickname "lucas123"
