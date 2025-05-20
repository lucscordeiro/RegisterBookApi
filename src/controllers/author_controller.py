from flask_restx import Namespace, Resource, fields
from flask import Blueprint, request
from services.author_service import AuthorService
from utils.response import response


api = Namespace('authors', description='Author related operations')


author_model = api.model('Author', {
    'first_name': fields.String(required=True, description='The first name of the author'),
    'last_name': fields.String(required=True, description='The last name of the author'),
    'bio': fields.String(required=False, description='A short biography of the author'),
})

@api.route('/')
class AuthorList(Resource):
    @api.doc('create_author')
    @api.expect(author_model)
    @api.response(201, 'Author created')
    @api.response(400, 'Failed to create author')
    def post(self):
        """Create a new author"""
        data = request.get_json()
        try:
            author = AuthorService.create_author(
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                bio=data.get('bio')
            )
            if author:
                return response(
                    status=201,
                    name_of_content='author',
                    content={
                        'author_id': author.author_id,
                        'first_name': author.first_name,
                        'last_name': author.last_name,
                        'bio': author.bio
                    }
                )
            else:
                return response(
                    status=400,
                    name_of_content='error',
                    content={},
                    message='Failed to create author'
                )
        except Exception as e:
            return response(
                status=400,
                name_of_content='error',
                content={},
                message=str(e)
            )

    @api.doc('get_all_authors')
    @api.response(200, 'List of authors')
    @api.response(400, 'Failed to fetch authors')
    def get(self):
        """Get a list of all authors"""
        authors = AuthorService.get_all_authors()
        return response(
            status=200,
            name_of_content='authors',
            content=[{
                'author_id': author.author_id,
                'first_name': author.first_name,
                'last_name': author.last_name,
                'bio': author.bio
            } for author in authors]
        )


@api.route('/<int:author_id>')
@api.response(404, 'Author not found')
class AuthorResource(Resource):
    @api.doc('get_author')
    @api.response(200, 'Author details')
    @api.response(404, 'Author not found')
    def get(self, author_id):
        """Fetch an author by ID"""
        author = AuthorService.get_author_by_id(author_id)
        if author:
            return response(
                status=200,
                name_of_content='author',
                content={
                    'author_id': author.author_id,
                    'first_name': author.first_name,
                    'last_name': author.last_name,
                    'bio': author.bio
                }
            )
        else:
            return response(
                status=404,
                name_of_content='error',
                content={},
                message='Author not found'
            )

    @api.doc('update_author')
    @api.expect(author_model)
    @api.response(200, 'Author updated')
    @api.response(404, 'Author not found')
    @api.response(400, 'Failed to update author')
    def put(self, author_id):
        """Update an existing author"""
        data = request.get_json()
        try:
            author = AuthorService.update_author(author_id, **data)
            if author:
                return response(
                    status=200,
                    name_of_content='author',
                    content={
                        'author_id': author.author_id,
                        'first_name': author.first_name,
                        'last_name': author.last_name,
                        'bio': author.bio
                    }
                )
            else:
                return response(
                    status=404,
                    name_of_content='error',
                    content={},
                    message='Author not found'
                )
        except Exception as e:
            return response(
                status=400,
                name_of_content='error',
                content={},
                message=str(e)
            )

    @api.doc('delete_author')
    @api.response(204, 'Author deleted')
    @api.response(404, 'Author not found')
    @api.response(400, 'Failed to delete author')
    def delete(self, author_id):
        """Delete an author by ID"""
        try:
            success = AuthorService.delete_author(author_id)
            if success:
                return response(
                    status=204,
                    name_of_content='message',
                    content={},
                    message='Author deleted successfully'
                )
            else:
                return response(
                    status=404,
                    name_of_content='error',
                    content={},
                    message='Author not found'
                )
        except Exception as e:
            return response(
                status=400,
                name_of_content='error',
                content={},
                message=str(e)
            )
