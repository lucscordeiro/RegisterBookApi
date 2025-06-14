Feature: Atualizar livro

  Scenario: Usuário atualiza a sinopse de um livro
    Given que a API está rodando
    When eu atualizo a sinopse do livro para "Nova sinopse atualizada"
    Then o livro deve ser atualizado com sucesso com status 200
    And a sinopse do livro deve ser "Nova sinopse atualizada"
