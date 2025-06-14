Feature: Buscar livro por ID

  Scenario: Usuário busca livro pelo ID
    Given que a API está rodando
    When eu busco o livro com id "1"
    Then o livro deve ser retornado com status 200
    And o título do livro deve ser "Clean Code"
