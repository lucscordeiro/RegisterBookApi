Feature: Gerenciamento de livros do usuário

    Scenario: Usuário adiciona um livro à sua lista
    Given que a API está rodando para user book
    When eu adiciono o livro com id "1" para o usuário com id "1" com progresso "25.5", nota "4", anotações "Gostei muito" e favorito "True"
    Then o livro deve ser adicionado com sucesso com status 201
    And o progresso do livro deve ser "25.5"
