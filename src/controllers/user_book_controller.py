from flask_restx import Namespace, Resource, fields
from services.user_book_service import UserBookService
from utils.response import response
from flask import request

api = Namespace('user_books', description='User-Book related operations')

user_book_model = api.model('UserBook', {
    'user_id': fields.Integer(required=True, description='The ID of the user'),
    'book_id': fields.Integer(required=True, description='The ID of the book'),
    'progress': fields.Float(required=False, description='Reading progress of the book'),
    'rating': fields.Integer(required=False, description='Rating given by the user'),
    'notes': fields.String(required=False, description='Additional notes about the book'),
    'favorite': fields.Boolean(required=False, description='Mark the book as favorite')  
})

@api.route('/')
class UserBookList(Resource):
    @api.doc('add_user_book')
    @api.expect(user_book_model)
    @api.response(201, 'UserBook added successfully')
    @api.response(400, 'Failed to add user book')
    def post(self):
        """Add a new UserBook entry"""
        data = request.get_json()
        try:
            user_book = UserBookService.add_user_book(
                user_id=data.get('user_id'),
                book_id=data.get('book_id'),
                progress=data.get('progress', 0.0),
                rating=data.get('rating'),
                notes=data.get('notes'),
                favorite=data.get('favorite', False)  
            )
            if user_book:
                return response(
                    status=201,
                    name_of_content='user_book',
                    content={
                        'user_book_id': user_book.user_book_id,
                        'user_id': user_book.user_id,
                        'book_id': user_book.book_id,
                        'progress': user_book.progress,
                        'rating': user_book.rating,
                        'notes': user_book.notes,
                        'favorite': user_book.favorite 
                    }
                )
            else:
                return response(
                    status=400,
                    name_of_content='error',
                    content={},
                    message='Failed to add user book'
                )
        except Exception as e:
            return response(
                status=400,
                name_of_content='error',
                content={},
                message=str(e)
            )

@api.route('/<int:user_book_id>')
@api.response(404, 'UserBook not found')
class UserBookResource(Resource):
    @api.doc('get_user_book')
    @api.response(200, 'UserBook details retrieved')
    def get(self, user_book_id):
        """Fetch a UserBook by ID"""
        user_book = UserBookService.get_user_book(user_book_id)
        if user_book:
            return response(
                status=200,
                name_of_content='user_book',
                content={
                    'user_book_id': user_book.user_book_id,
                    'user_id': user_book.user_id,
                    'book_id': user_book.book_id,
                    'progress': user_book.progress,
                    'rating': user_book.rating,
                    'notes': user_book.notes,
                    'favorite': user_book.favorite  
                }
            )
        else:
            return response(
                status=404,
                name_of_content='error',
                content={},
                message='UserBook not found'
            )

    @api.doc('update_user_book')
    @api.expect(user_book_model)
    @api.response(200, 'UserBook updated successfully')
    @api.response(400, 'Failed to update user book')
    def put(self, user_book_id):
        """Update an existing UserBook entry"""
        data = request.get_json()
        try:
            user_book = UserBookService.update_user_book(user_book_id, **data)
            if user_book:
                return response(
                    status=200,
                    name_of_content='user_book',
                    content={
                        'user_book_id': user_book.user_book_id,
                        'user_id': user_book.user_id,
                        'book_id': user_book.book_id,
                        'progress': user_book.progress,
                        'rating': user_book.rating,
                        'notes': user_book.notes,
                        'favorite': user_book.favorite  
                    }
                )
            else:
                return response(
                    status=404,
                    name_of_content='error',
                    content={},
                    message='UserBook not found'
                )
        except Exception as e:
            return response(
                status=400,
                name_of_content='error',
                content={},
                message=str(e)
            )

    @api.doc('delete_user_book')
    @api.response(204, 'UserBook deleted successfully')
    @api.response(400, 'Failed to delete user book')
    def delete(self, user_book_id):
        """Delete a UserBook entry by ID"""
        try:
            success = UserBookService.delete_user_book(user_book_id)
            if success:
                return response(
                    status=204,
                    name_of_content='message',
                    content={},
                    message='UserBook deleted successfully'
                )
            else:
                return response(
                    status=404,
                    name_of_content='error',
                    content={},
                    message='UserBook not found'
                )
        except Exception as e:
            return response(
                status=400,
                name_of_content='error',
                content={},
                message=str(e)
            )

@api.route('/user/<int:user_id>')
@api.response(404, 'No user books found for this user')
class UserBooksByUser(Resource):
    @api.doc('get_all_user_books_by_user')
    @api.response(200, 'UserBooks retrieved successfully')
    def get(self, user_id):
        """Fetch all UserBooks for a specific user"""
        user_books = UserBookService.get_all_user_books_by_user(user_id)
        if user_books:
            return response(
                status=200,
                name_of_content='user_books',
                content=[
                    {
                        'user_book_id': ub.user_book_id,
                        'user_id': ub.user_id,
                        'book_id': ub.book_id,
                        'progress': ub.progress,
                        'rating': ub.rating,
                        'notes': ub.notes,
                        'favorite': ub.favorite  
                    } for ub in user_books
                ]
            )
        else:
            return response(
                status=404,
                name_of_content='error',
                content={},
                message='No user books found for this user'
            )

@api.route('/<int:user_book_id>/favorite')
class MarkAsFavorite(Resource):
    @api.doc('mark_as_favorite')
    @api.response(200, 'UserBook marked as favorite successfully')
    @api.response(400, 'Failed to mark user book as favorite')
    def post(self, user_book_id):
        """Mark a UserBook as favorite"""
        try:
            user_book = UserBookService.mark_as_favorite(user_book_id, favorite=True)
            if user_book:
                return response(
                    status=200,
                    name_of_content='user_book',
                    content={
                        'user_book_id': user_book.user_book_id,
                        'user_id': user_book.user_id,
                        'book_id': user_book.book_id,
                        'progress': user_book.progress,
                        'rating': user_book.rating,
                        'notes': user_book.notes,
                        'favorite': user_book.favorite
                    }
                )
            else:
                return response(
                    status=404,
                    name_of_content='error',
                    content={},
                    message='UserBook not found'
                )
        except Exception as e:
            return response(
                status=400,
                name_of_content='error',
                content={},
                message=str(e)
            )
    @api.route('/user/<int:user_id>/complete-books')
    @api.response(404, 'No books found for this user')
    class UserCompleteBooksByUser(Resource):
        @api.doc('get_complete_books_by_user')
        @api.response(200, 'Complete books retrieved successfully')
        def get(self, user_id):
            """Fetch all complete books for a specific user"""
            books = UserBookService.get_complete_books_by_user(user_id)
            if books:
                return response(
                    status=200,
                    name_of_content='books',
                    content=books
                )
            else:
                return response(
                    status=404,
                    name_of_content='error',
                    content={},
                    message='No books found for this user'
                )