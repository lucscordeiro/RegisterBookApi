Feature: Deletar livro

  Scenario: Usuário deleta um livro pelo ID
    Given que a API está rodando
    When eu deleto o livro com id "1"
    Then o livro deve ser deletado com sucesso com status 204
