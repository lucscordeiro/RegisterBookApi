from extensions import db
from sqlalchemy.exc import SQLAlchemyError
from models import WeekRecomendation, Book

class WeekRecomendationService:
    @staticmethod
    def create_recomendation(book_id, title, citation):
        try:
            recomendation = WeekRecomendation(
                book_id=book_id,
                title=title,
                citation=citation
            )
            db.session.add(recomendation)
            db.session.commit()
            return recomendation
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error creating week recomendation: {e}")
            return None

    @staticmethod
    def get_recomendation_by_id(recomendation_id):
        try:
            return WeekRecomendation.query.get(recomendation_id)
        except SQLAlchemyError as e:
            print(f"Error finding week recomendation: {e}")
            return None

    @staticmethod
    def update_recomendation(recomendation_id, **kwargs):
        try:
            recomendation = WeekRecomendation.query.get(recomendation_id)
            if not recomendation:
                print("Week recomendation not found")
                return None
            for key, value in kwargs.items():
                if hasattr(recomendation, key):
                    setattr(recomendation, key, value)
            db.session.commit()
            return recomendation
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error updating week recommendation: {e}")
            return None

    @staticmethod
    def delete_recomendation(recomendation_id):
        try:
            recomendation = WeekRecomendation.query.get(recomendation_id)
            if not recomendation:
                print("Week recomendation not found")
                return None
            db.session.delete(recomendation)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error deleting week recomendation: {e}")
            return None

    @staticmethod
    def get_recomendations_for_book(book_id):
        try:
            return WeekRecomendation.query.filter_by(book_id=book_id).all()
        except SQLAlchemyError as e:
            print(f"Error retrieving recomendations for book: {e}")
            return None
        
    @staticmethod
    def get_latest_recomendation():
        try:
            return WeekRecomendation.query.order_by(WeekRecomendation.recomendation_id.desc()).first()
        except SQLAlchemyError as e:
            print(f"Error retrieving latest week recomendation: {e}")
            return None