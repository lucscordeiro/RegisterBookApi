from flask_restx import Namespace, Resource

api = Namespace('health', description='Health check endpoint')

@api.route('/')
class HealthResource(Resource):
    def get(self):
        return {'status': 'ok'}, 200
