
from extensions import db
from models import Genre
from sqlalchemy.exc import SQLAlchemyError

class GenreService:

    @staticmethod
    def get_genre_by_id(genre_id):
        try:
            genre = Genre.query.get(genre_id)
            if genre is None:
                raise ValueError(f"Genre with ID {genre_id} does not exist.")
            return genre
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error retrieving genre by ID: {e}")
            raise e
        except ValueError as e:
            print(e)
            raise e

    @staticmethod
    def create_genre(name):
        try:
            existing_genre = Genre.query.filter_by(name=name).first()
            if existing_genre:
                return existing_genre
            
            genre = Genre(name=name)
            db.session.add(genre)
            db.session.commit()
            return genre
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error creating genre: {e}")
            raise e
        except Exception as e:
            db.session.rollback()
            print(f"Unexpected error creating genre: {e}")
            raise e

    @staticmethod
    def get_all_genres():
        try:
            return Genre.query.all()
        except SQLAlchemyError as e:
            print(f"Error retrieving all genres: {e}")
            raise e

    @staticmethod
    def update_genre(genre_id, name):
        try:
            genre = Genre.query.get(genre_id)
            if genre is None:
                raise ValueError(f"Genre with ID {genre_id} does not exist.")
            genre.name = name
            db.session.commit()
            return genre
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error updating genre: {e}")
            raise e
        except ValueError as e:
            print(e)
            raise e

    @staticmethod
    def delete_genre(genre_id):
        try:
            genre = Genre.query.get(genre_id)
            if genre is None:
                raise ValueError(f"Genre with ID {genre_id} does not exist.")
            db.session.delete(genre)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error deleting genre: {e}")
            raise e
        except ValueError as e:
            print(e)
            raise e
