from extensions import db
from sqlalchemy.exc import SQLAlchemyError
from models import UserBook, Book
from sqlalchemy.orm import joinedload
from services.book_service import BookService

class UserBookService:
    @staticmethod
    def add_user_book(user_id, book_id, progress=0.0, rating=None, notes=None, favorite=False):
        try:
            user_book = UserBook(
                user_id=user_id,
                book_id=book_id,
                progress=progress,
                rating=rating,
                notes=notes,
                favorite=favorite  
            )
            db.session.add(user_book)
            db.session.commit()
            return user_book
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error adding user book: {e}")
            return None

    @staticmethod
    def get_user_book(user_book_id):
        try:
            return UserBook.query.get(user_book_id)
        except SQLAlchemyError as e:
            print(f"Error finding user book: {e}")
            return None

    @staticmethod
    def update_user_book(user_book_id, **kwargs):
        try:
            user_book = UserBook.query.get(user_book_id)
            if not user_book:
                print("UserBook not found")
                return None
            for key, value in kwargs.items():
                if hasattr(user_book, key):
                    setattr(user_book, key, value)
            db.session.commit()
            return user_book
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error updating user book: {e}")
            return None

    @staticmethod
    def delete_user_book(user_book_id):
        try:
            user_book = UserBook.query.get(user_book_id)
            if not user_book:
                print("UserBook not found")
                return None
            db.session.delete(user_book)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error deleting user book: {e}")
            return None

    @staticmethod
    def get_all_user_books_by_user(user_id):
        try:
            return UserBook.query.filter_by(user_id=user_id).all()
        except SQLAlchemyError as e:
            print(f"Error retrieving user books: {e}")
            return None

    @staticmethod
    def mark_as_favorite(user_book_id, favorite=True):
        try:
            user_book = UserBook.query.get(user_book_id)
            if not user_book:
                print("UserBook not found")
                return None
            user_book.favorite = favorite
            db.session.commit()
            return user_book
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error marking book as favorite: {e}")
            return None
        
    @staticmethod
    def get_complete_books_by_user(user_id):
        try:
            user_books = (
                db.session.query(UserBook)
                .filter(UserBook.user_id == user_id)
                .all()
            )
            
            books = []
            for user_book in user_books:
                book = BookService.get_book_by_id(user_book.book_id)
                if book:
                    book_data = {
                        'book_id': book.book_id,
                        'title': book.title,
                        'publisher_id': book.publisher_id,
                        'cover_image': book.cover_image,
                        'author_id': book.author_id,
                        'synopsis': book.synopsis,
                        'progress': user_book._progress,
                        'rating': user_book._rating,
                        'notes': user_book.notes,
                        'favorite': user_book.favorite,
                        'user_book_id': user_book.user_book_id,
                    }
                    books.append(book_data)
                
            return books
        except Exception as e:
            print(f"Error retrieving books for user {user_id}: {e}")
            return None