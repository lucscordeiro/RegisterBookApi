from models import User
from extensions import db
from sqlalchemy.exc import SQLAlchemyError

class UserService:

    @staticmethod
    def create_user(first_name, last_name, nickname, cpf, phone_number, password, profile_picture="", quote=""):
        if not all([first_name, last_name, nickname, cpf, phone_number, password]):
            raise ValueError("All fields are required except phone_number, profile_picture, and quote.")
        if User.query.filter_by(cpf=cpf).first() or User.query.filter_by(nickname=nickname).first():
            print("User with the given CPF or nickname already exists.")
            return None
        try:
            user = User(
                first_name=first_name,
                last_name=last_name,
                nickname=nickname,
                cpf=cpf,
                phone_number=phone_number,
                profile_picture=profile_picture,
                quote=quote
            )
            user.set_password(password)  
            db.session.add(user)
            db.session.commit()
            return user
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error creating user, try again\n{e}")
            return None

    @staticmethod
    def get_user_by_id(user_id):
        try:
            return User.query.get(user_id)
        except SQLAlchemyError as e:
            print(f"Error finding user: {e}")
            return None

    @staticmethod
    def update_user(user_id, **kwargs):
        try:
            user = User.query.get(user_id)
            if not user:
                print("User not found")
                return None
            for key, value in kwargs.items():
                if hasattr(user, key):
                    if key == 'password':  
                        user.set_password(value)
                    else:
                        setattr(user, key, value)
            db.session.commit()
            return user
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error updating user: {e}")
            return None

    @staticmethod
    def delete_user(user_id):
        try:
            user = User.query.get(user_id)
            if not user:
                print("User not found")
                return None
            db.session.delete(user)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error deleting user: {e}")
            return None

    @staticmethod
    def authenticate_user(cpf_or_nickname, password):
        try:
            user = User.query.filter((User.cpf == cpf_or_nickname) | (User.nickname == cpf_or_nickname)).first()
            if user and user.check_password(password):
                return user
            return None
        except SQLAlchemyError as e:
            print(f"Error authenticating user: {e}")
            return None
        
