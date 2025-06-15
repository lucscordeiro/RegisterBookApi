Feature: Deletar livro

  Scenario: Usuário deleta um livro pelo ID
    Given que a API está rodando
    When eu deleto o livro com id "1"
    Then o livro deve ser deletado com sucesso com status 204

  Scenario: Usuário tenta deletar um livro com ID inexistente
      Given que a API está rodando
      When eu deleto o livro com id "9999"
      Then devo receber uma resposta de erro com status 404