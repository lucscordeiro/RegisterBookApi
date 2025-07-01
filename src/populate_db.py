from app import create_app
from extensions import db
from models import Book, Author, Publisher

app = create_app()

with app.app_context():

    # Verifica e cria Autor com author_id=1 se não existir
    author = Author.query.get(1)
    if not author:
        author = Author(author_id=1, first_name="Autor", last_name="Teste", bio="Autor para testes")
        db.session.add(author)
        print("Autor criado")

    # Verifica e cria Editora com publisher_id=1 se não existir
    publisher = Publisher.query.get(1)
    if not publisher:
        publisher = Publisher(publisher_id=1, name="Editora Teste")
        db.session.add(publisher)
        print("Editora criada")

    db.session.commit()

    # Popula o banco com 10.000 livros
    for i in range(10000):
        book = Book(
            title=f"Livro Volume {i}",
            publisher_id=publisher.publisher_id, 
            author_id=author.author_id,           
            cover_image="http://example.com/img.jpg",
            synopsis="Teste volume"
        )
        db.session.add(book)

        if i % 1000 == 0 and i != 0:
            db.session.commit()
            print(f"Commitado até o livro {i}")

    db.session.commit()
    print("População dos livros concluída com sucesso!")
