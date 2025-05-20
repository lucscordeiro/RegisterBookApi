from flask import Blueprint, request
from flask_restx import Namespace, Resource, fields
from services.week_recomendation_service import WeekRecomendationService
from utils.response import response

api = Namespace('week_recomendations', description='Week Recomendation related operations')

recomendation_model = api.model('Recomendation', {
    'book_id': fields.Integer(required=True, description='The ID of the book'),
    'citation': fields.String(required=True, description='A citation from the book'),
    'title': fields.String(required=True, description='Title of the recomendation'),
})

@api.route('/')
class RecomendationList(Resource):
    @api.doc('create_recomendation')
    @api.expect(recomendation_model)
    @api.response(201, 'Recomendation created')
    @api.response(400, 'Failed to create recomendation')
    def post(self):
        """Create a new week recomendation"""
        data = request.get_json()
        try:
            recomendation = WeekRecomendationService.create_recomendation(
                book_id=data.get('book_id'),
                citation=data.get('citation'),
                title=data.get('title')
            )
            if recomendation:
                return response(
                    status=201,
                    name_of_content='recomendation',
                    content={
                        'recomendation_id': recomendation.recomendation_id,
                        'book_id': recomendation.book_id,
                        'citation': recomendation.citation,
                        'title': recomendation.title
                    }
                )
            else:
                return response(
                    status=400,
                    name_of_content='error',
                    content={},
                    message='Failed to create recomendation'
                )
        except Exception as e:
            return response(
                status=400,
                name_of_content='error',
                content={},
                message=str(e)
            )

    @api.doc('get_all_recomendations')
    @api.response(200, 'Recomendations retrieved successfully')
    def get(self):
        """Get all week recomendations"""
        recomendations = WeekRecomendationService.get_all_recomendations()
        return response(
            status=200,
            name_of_content='recomendations',
            content=[{
                'recomendation_id': recomendation.recomendation_id,
                'book_id': recomendation.book_id,
                'citation': recomendation.citation,
                'title': recomendation.title
            } for recomendation in recomendations]
        )


@api.route('/<int:recomendation_id>')
@api.response(404, 'Recomendation not found')
class RecomendationResource(Resource):
    @api.doc('get_recomendation')
    @api.response(200, 'Recomendation details')
    def get(self, recomendation_id):
        """Fetch a recomendation by ID"""
        recomendation = WeekRecomendationService.get_recomendation_by_id(recomendation_id)
        if recomendation:
            return response(
                status=200,
                name_of_content='recomendation',
                content={
                    'recomendation_id': recomendation.recomendation_id,
                    'book_id': recomendation.book_id,
                    'citation': recomendation.citation,
                    'title': recomendation.title
                }
            )
        else:
            return response(
                status=404,
                name_of_content='error',
                content={},
                message='Recomendation not found'
            )

    @api.doc('update_recomendation')
    @api.expect(recomendation_model)
    @api.response(200, 'Recomendation updated')
    @api.response(400, 'Failed to update recomendation')
    def put(self, recomendation_id):
        """Update an existing recomendation"""
        data = request.get_json()
        try:
            recomendation = WeekRecomendationService.update_recomendation(
                recomendation_id,
                book_id=data.get('book_id'),
                citation=data.get('citation'),
                title=data.get('title')
            )
            if recomendation:
                return response(
                    status=200,
                    name_of_content='recomendation',
                    content={
                        'recomendation_id': recomendation.recomendation_id,
                        'book_id': recomendation.book_id,
                        'citation': recomendation.citation,
                        'title': recomendation.title
                    }
                )
            else:
                return response(
                    status=404,
                    name_of_content='error',
                    content={},
                    message='Recomendation not found'
                )
        except Exception as e:
            return response(
                status=400,
                name_of_content='error',
                content={},
                message=str(e)
            )

    @api.doc('delete_recomendation')
    @api.response(204, 'Recomendation deleted')
    @api.response(400, 'Failed to delete recomendation')
    def delete(self, recomendation_id):
        """Delete a recomendation by ID"""
        try:
            success = WeekRecomendationService.delete_recomendation(recomendation_id)
            if success:
                return response(
                    status=204,
                    name_of_content='message',
                    content={},
                    message='Recomendation deleted successfully'
                )
            else:
                return response(
                    status=404,
                    name_of_content='error',
                    content={},
                    message='Recomendation not found'
                )
        except Exception as e:
            return response(
                status=400,
                name_of_content='error',
                content={},
                message=str(e)
            )



@api.route('/latest')
class LatestRecomendation(Resource):
    @api.doc('get_latest_recomendation')
    @api.response(200, 'Latest recomendation retrieved successfully')
    @api.response(404, 'No recomendations found')
    def get(self):
        """Get the latest week recomendation"""
        try:
            recomendation = WeekRecomendationService.get_latest_recomendation()
            if recomendation:
                return response(
                    status=200,
                    name_of_content='recomendation',
                    content={
                        'recomendation_id': recomendation.recomendation_id,
                        'book_id': recomendation.book_id,
                        'citation': recomendation.citation,
                        'title': recomendation.title
                    }
                )
            else:
                return response(
                    status=404,
                    name_of_content='error',
                    content={},
                    message='No recomendations found'
                )
        except Exception as e:
            return response(
                status=400,
                name_of_content='error',
                content={},
                message=str(e)
            )
