from extensions import db
from sqlalchemy.exc import SQLAlchemyError
from models import Author

class AuthorService:
    @staticmethod
    def create_author(first_name, last_name, bio):
        try:
            author = Author(
                first_name=first_name,
                last_name=last_name,
                bio=bio
            )
            db.session.add(author)
            db.session.commit()
            return author
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error creating author: {e}")
            return None

    @staticmethod
    def get_author_by_id(author_id):
        try:
            return Author.query.get(author_id)
        except SQLAlchemyError as e:
            print(f"Error finding author: {e}")
            return None

    @staticmethod
    def update_author(author_id, **kwargs):
        try:
            author = Author.query.get(author_id)
            if not author:
                print("Author not found")
                return None
            for key, value in kwargs.items():
                if hasattr(author, key):
                    setattr(author, key, value)
            db.session.commit()
            return author
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error updating author: {e}")
            return None

    @staticmethod
    def delete_author(author_id):
        try:
            author = Author.query.get(author_id)
            if not author:
                print("Author not found")
                return None
            db.session.delete(author)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error deleting author: {e}")
            return None

    @staticmethod
    def get_all_authors():
        try:
            return Author.query.order_by(Author.first_name.asc()).all()
        except SQLAlchemyError as e:
            print(f"Error retrieving authors: {e}")
            return []
