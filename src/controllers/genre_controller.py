from flask import Blueprint, request
from flask_restx import Namespace, Resource, fields
from services.genre_service import GenreService
from utils.response import response

api = Namespace('genres', description='Genre related operations')

genre_model = api.model('Genre', {
    'name': fields.String(required=True, description='The name of the genre'),
})

@api.route('/')
class GenreList(Resource):
    @api.doc('create_genre')
    @api.expect(genre_model)
    @api.response(201, 'Genre created')
    @api.response(400, 'Failed to create genre')
    def post(self):
        """Create a new genre"""
        data = request.get_json()
        try:
            genre = GenreService.create_genre(name=data.get('name'))
            if genre:
                return response(
                    status=201,
                    name_of_content='genre',
                    content={
                        'genre_id': genre.genre_id,
                        'name': genre.name
                    }
                )
            else:
                return response(
                    status=400,
                    name_of_content='error',
                    content={},
                    message='Failed to create genre'
                )
        except Exception as e:
            return response(
                status=400,
                name_of_content='error',
                content={},
                message=str(e)
            )

    @api.doc('get_all_genres')
    @api.response(200, 'Genres finded successfully')
    def get(self):
        """Fetch all genres"""
        genres = GenreService.get_all_genres()
        return response(
            status=200,
            name_of_content='genres',
            content=[{
                'genre_id': genre.genre_id,
                'name': genre.name
            } for genre in genres]
        )


@api.route('/<int:genre_id>')
@api.response(404, 'Genre not found')
class GenreResource(Resource):
    @api.doc('get_genre')
    @api.response(200, 'Genre details')
    def get(self, genre_id):
        """Fetch a genre by ID"""
        genre = GenreService.get_genre_by_id(genre_id)
        if genre:
            return response(
                status=200,
                name_of_content='genre',
                content={
                    'genre_id': genre.genre_id,
                    'name': genre.name
                }
            )
        else:
            return response(
                status=404,
                name_of_content='error',
                content={},
                message='Genre not found'
            )

    @api.doc('update_genre')
    @api.expect(genre_model)
    @api.response(200, 'Genre updated')
    @api.response(400, 'Failed to update genre')
    def put(self, genre_id):
        """Update an existing genre"""
        data = request.get_json()
        try:
            genre = GenreService.update_genre(genre_id, name=data.get('name'))
            if genre:
                return response(
                    status=200,
                    name_of_content='genre',
                    content={
                        'genre_id': genre.genre_id,
                        'name': genre.name
                    }
                )
            else:
                return response(
                    status=404,
                    name_of_content='error',
                    content={},
                    message='Genre not found'
                )
        except Exception as e:
            return response(
                status=400,
                name_of_content='error',
                content={},
                message=str(e)
            )

    @api.doc('delete_genre')
    @api.response(204, 'Genre deleted')
    @api.response(400, 'Failed to delete genre')
    def delete(self, genre_id):
        """Delete a genre by ID"""
        try:
            success = GenreService.delete_genre(genre_id)
            if success:
                return response(
                    status=204,
                    name_of_content='message',
                    content={},
                    message='Genre deleted successfully'
                )
            else:
                return response(
                    status=404,
                    name_of_content='error',
                    content={},
                    message='Genre not found'
                )
        except Exception as e:
            return response(
                status=400,
                name_of_content='error',
                content={},
                message=str(e)
            )
