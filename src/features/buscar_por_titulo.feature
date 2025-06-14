Feature: Buscar livros por título

  Scenario: Usuário busca livros que contenham uma palavra no título
    Given que a API está rodando
    And que um livro com título "Clean Code" está cadastrado
    When eu busco livros com título contendo "Clean"
    Then a API deve retornar uma lista de livros com status 200
    And pelo menos um livro deve conter "Clean" no título

