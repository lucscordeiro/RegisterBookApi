from flask import Blueprint, request
from flask_restx import Namespace, Resource, fields
from services.book_service import BookService
from utils.response import response

api = Namespace('books', description='Book related operations')

book_model = api.model('Book', {
    'title': fields.String(required=True, description='The title of the book'),
    'publisher_id': fields.Integer(required=True, description='The ID of the publisher'),
    'cover_image': fields.String(required=False, description='URL of the cover image'),
    'author_id': fields.Integer(required=True, description='The ID of the author'),
    'synopsis': fields.String(required=False, description='A short synopsis of the book'),
    'genre_id': fields.Integer(required=False, description='The ID of the genre'),
})

@api.route('/')
class BookList(Resource):
    @api.doc('create_book')
    @api.expect(book_model)
    @api.response(201, 'Book created')
    @api.response(400, 'Failed to create book')
    def post(self):
        """Create a new book"""
        data = request.get_json()
        try:
            book = BookService.create_book(
                title=data.get('title'),
                publisher_id=data.get('publisher_id'),
                cover_image=data.get('cover_image'),
                author_id=data.get('author_id'),
                synopsis=data.get('synopsis')
            )
            genre_id = data.get('genre_id')
            if genre_id:
                BookService.add_genre_to_book(book.book_id, genre_id)
            
            if book:
                return response(
                    status=201,
                    name_of_content='book',
                    content={
                        'book_id': book.book_id,
                        'title': book.title,
                        'publisher_id': book.publisher_id,
                        'cover_image': book.cover_image,
                        'author_id': book.author_id,
                        'synopsis': book.synopsis
                    }
                )
            else:
                return response(
                    status=400,
                    name_of_content='error',
                    content={},
                    message='Failed to create book'
                )
        except Exception as e:
            return response(
                status=400,
                name_of_content='error',
                content={},
                message=str(e)
            )
@api.route('/list')
class BookListByQuantity(Resource):
    @api.doc('get_books_by_quantity')
    @api.param('quantity', 'Number of books to retrieve')
    @api.response(200, 'Books retrieved successfully')
    @api.response(400, 'Failed to retrieve books')
    def get(self):
        """Fetch a specific number of random books based on the quantity"""
        quantity = request.args.get('quantity', default=10, type=int)  
        try:
            if quantity > 100:
                return response(
                    status=400,
                    name_of_content='error',
                    content={},
                    message='Invalid quantity. Please choose a quantity less than 100.'
                )
            
            books = BookService.get_books(quantity)

            if books is None:
                return response(
                    status=400,
                    name_of_content='error',
                    content={},
                    message='Failed to retrieve books.'
                )

            return response(
                status=200,
                name_of_content='books',
                content=[{
                    'book_id': book.book_id,
                    'title': book.title,
                    'publisher_id': book.publisher_id,
                    'cover_image': book.cover_image,
                    'author_id': book.author_id,
                    'synopsis': book.synopsis
                } for book in books]
            )
        except Exception as e:
            return response(
                status=400,
                name_of_content='error',
                content={},
                message=str(e)
            )
    
            
@api.route('/<int:book_id>')
@api.response(404, 'Book not found')
class BookResource(Resource):
    @api.doc('get_book')
    @api.response(200, 'Book details')
    def get(self, book_id):
        """Fetch a book by ID"""
        book = BookService.get_book_by_id(book_id)
        if book:
            return response(
                status=200,
                name_of_content='book',
                content={
                    'book_id': book.book_id,
                    'title': book.title,
                    'publisher_id': book.publisher_id,
                    'cover_image': book.cover_image,
                    'author_id': book.author_id,
                    'synopsis': book.synopsis
                }
            )
        else:
            return response(
                status=404,
                name_of_content='error',
                content={},
                message='Book not found'
            )

    @api.doc('update_book')
    @api.expect(book_model)
    @api.response(200, 'Book updated')
    @api.response(400, 'Failed to update book')
    def put(self, book_id):
        """Update an existing book"""
        data = request.get_json()
        try:
            book = BookService.update_book(book_id, **data)
            if book:
                return response(
                    status=200,
                    name_of_content='book',
                    content={
                        'book_id': book.book_id,
                        'title': book.title,
                        'publisher_id': book.publisher_id,
                        'cover_image': book.cover_image,
                        'author_id': book.author_id,
                        'synopsis': book.synopsis
                    }
                )
            else:
                return response(
                    status=404,
                    name_of_content='error',
                    content={},
                    message='Book not found'
                )
        except Exception as e:
            return response(
                status=400,
                name_of_content='error',
                content={},
                message=str(e)
            )

    @api.doc('delete_book')
    @api.response(204, 'Book deleted')
    @api.response(400, 'Failed to delete book')
    def delete(self, book_id):
        """Delete a book by ID"""
        try:
            success = BookService.delete_book(book_id)
            if success:
                return response(
                    status=204,
                    name_of_content='message',
                    content={},
                    message='Book deleted successfully'
                )
            else:
                return response(
                    status=404,
                    name_of_content='error',
                    content={},
                    message='Book not found'
                )
        except Exception as e:
            return response(
                status=400,
                name_of_content='error',
                content={},
                message=str(e)
            )


@api.route('/list/genre/<int:genre_id>')
class BooksByGenre(Resource):
    @api.doc('get_books_by_genre')
    @api.response(200, 'Books retrieved successfully')
    @api.response(400, 'Failed to retrieve books')
    def get(self, genre_id):
        """Fetch books by genre"""
        try:
            books = BookService.get_books_by_genre(genre_id)

            if not books:
                return response(
                    status=404,
                    name_of_content='error',
                    content={},
                    message='No books found for this genre'
                )

            return response(
                status=200,
                name_of_content='books',
                content=[{
                    'book_id': book.book_id,
                    'title': book.title,
                    'publisher_id': book.publisher_id,
                    'cover_image': book.cover_image,
                    'author': {
                        'author_id': book.author.author_id,
                        'first_name': book.author.first_name,
                        'last_name': book.author.last_name,
                        'bio': book.author.bio
                    },
                    'genres': [{'genre_id': genre.genre_id, 'name': genre.name} for genre in book.genres],
                    'synopsis': book.synopsis
                } for book in books]
            )
        except Exception as e:
            return response(
                status=400,
                name_of_content='error',
                content={},
                message=str(e)
            )

@api.route('/list/author')
class BookListByAuthorAndGenre(Resource):
    @api.doc('get_books_with_author_and_genre')
    @api.param('quantity', 'Number of books to retrieve')
    @api.response(200, 'Books with authors and genres retrieved successfully')
    @api.response(400, 'Failed to retrieve books with authors and genres')
    def get(self):
        """Fetch a specific number of random books with their authors and genres"""
        quantity = request.args.get('quantity', default=10, type=int)  
        try:
            if quantity > 100:
                return response(
                    status=400,
                    name_of_content='error',
                    content={},
                    message='Invalid quantity. Please choose a quantity less than 100.'
                )
            
            books = BookService.get_books_with_author_and_genre(quantity)

            if books is None:
                return response(
                    status=400,
                    name_of_content='error',
                    content={},
                    message='Failed to retrieve books.'
                )

            return response(
                status=200,
                name_of_content='books',
                content=[{
                    'book_id': book.book_id,
                    'title': book.title,
                    'publisher_id': book.publisher_id,
                    'cover_image': book.cover_image,
                    'author': {
                        'author_id': book.author.author_id,
                        'first_name': book.author.first_name,
                        'last_name': book.author.last_name,
                        'bio': book.author.bio
                    },
                    'genres': [{'genre_id': genre.genre_id, 'name': genre.name} for genre in book.genres],
                    'synopsis': book.synopsis
                } for book in books]
            )
        except Exception as e:
            return response(
                status=400,
                name_of_content='error',
                content={},
                message=str(e)
            )
            
    @api.route('/search')
    class BookSearch(Resource):
        @api.doc('get_books_by_title')
        @api.param('title', 'Title of the book to search')
        @api.response(200, 'Books retrieved successfully')
        @api.response(400, 'Failed to retrieve books')
        def get(self):
            """Fetch books by title"""
            title = request.args.get('title', default='', type=str)
            try:
                books = BookService.get_books_by_title(title)
                
                if books is None:
                    return response(
                        status=400,
                        name_of_content='error',
                        content={},
                        message='Failed to retrieve books.'
                    )

                return response(
                    status=200,
                    name_of_content='books',
                    content=[{
                        'book_id': book.book_id,
                        'title': book.title,
                        'publisher_id': book.publisher_id,
                        'cover_image': book.cover_image,
                        'author': {
                            'author_id': book.author.author_id,
                            'first_name': book.author.first_name,
                            'last_name': book.author.last_name,
                            'bio': book.author.bio
                        },
                        'genres': [{'genre_id': genre.genre_id, 'name': genre.name} for genre in book.genres],
                        'synopsis': book.synopsis
                    } for book in books]
                )
            except Exception as e:
                return response(
                    status=400,
                    name_of_content='error',
                    content={},
                    message=str(e)
                )