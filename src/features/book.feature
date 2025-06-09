Feature: Cadastro de livros na API

  Scenario: Usuário cadastra um novo livro completo
    Given que a API está rodando
    When eu cadastro um livro com título "Clean Code", publisher_id "1", cover_image "http://example.com/cover.jpg", author_id "1", e sinopse "Um livro sobre código limpo"
    Then o livro deve ser cadastrado com sucesso com status 201
