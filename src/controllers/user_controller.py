from flask import request
from flask_restx import Namespace, Resource, fields
from services.user_service import UserService
from utils.response import response

api = Namespace('users', description='Operações relacionadas a usuários')


user_model = api.model('User', {
    'first_name': fields.String(required=True, description='Primeiro nome do usuário'),
    'last_name': fields.String(required=True, description='Último nome do usuário'),
    'nickname': fields.String(required=True, description='Apelido do usuário'),
    'cpf': fields.String(required=True, description='CPF do usuário'),
    'phone_number': fields.String(required=True, description='Número de telefone do usuário'),
    'profile_picture': fields.String(description='URL da foto de perfil do usuário'),
    'password': fields.String(required=True, description='Senha do usuário'),
    'quote': fields.String(description='Citação favorita do usuário')
})

login_model = api.model('Login', {
    'cpf_or_nickname': fields.String(required=True, description='CPF ou nickname do usuário'),
    'password': fields.String(required=True, description='Senha do usuário')
})

@api.route('/')
class UserList(Resource):
    @api.doc('create_user')
    @api.expect(user_model)
    @api.response(201, 'Usuário criado')
    @api.response(400, 'Falha ao criar usuário')
    def post(self):
        """Cria um novo usuário"""
        data = request.get_json()
        try:
            user = UserService.create_user(
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                nickname=data.get('nickname'),
                cpf=data.get('cpf'),
                phone_number=data.get('phone_number'),
                profile_picture=data.get('profile_picture'),
                password=data.get('password'),  
                quote=data.get('quote')
            )
            if user:
                return response(
                    status=201,
                    name_of_content='user',
                    content={
                        'user_id': user.user_id,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'nickname': user.nickname,
                        'cpf': user.cpf,
                        'phone_number': user.phone_number,
                        'profile_picture': user.profile_picture,
                        'quote': user.quote
                    }
                )
            else:
                return response(
                    status=400,
                    name_of_content='error',
                    content={},
                    message='Falha ao criar usuário'
                )
        except Exception as e:
            return response(
                status=400,
                name_of_content='error',
                content={},
                message=str(e)
            )

@api.route('/<int:user_id>')
@api.response(404, 'Usuário não encontrado')
class UserResource(Resource):
    @api.doc('get_user')
    @api.response(200, 'Detalhes do usuário')
    def get(self, user_id):
        """Obtém um usuário por ID"""
        user = UserService.get_user_by_id(user_id)
        if user:
            return response(
                status=200,
                name_of_content='user',
                content={
                    'user_id': user.user_id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'nickname': user.nickname,
                    'cpf': user.cpf,
                    'phone_number': user.phone_number,
                    'profile_picture': user.profile_picture,
                    'quote': user.quote
                }
            )
        else:
            return response(
                status=404,
                name_of_content='error',
                content={},
                message='Usuário não encontrado'
            )

    @api.doc('update_user')
    @api.expect(user_model)
    @api.response(200, 'Usuário atualizado')
    @api.response(400, 'Falha ao atualizar usuário')
    def put(self, user_id):
        """Atualiza um usuário existente"""
        data = request.get_json()
        try:
            user = UserService.update_user(user_id, **data)
            if user:
                return response(
                    status=200,
                    name_of_content='user',
                    content={
                        'user_id': user.user_id,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'nickname': user.nickname,
                        'cpf': user.cpf,
                        'phone_number': user.phone_number,
                        'profile_picture': user.profile_picture,
                        'quote': user.quote
                    }
                )
            else:
                return response(
                    status=404,
                    name_of_content='error',
                    content={},
                    message='Usuário não encontrado'
                )
        except Exception as e:
            return response(
                status=400,
                name_of_content='error',
                content={},
                message=str(e)
            )

    @api.doc('delete_user')
    @api.response(204, 'Usuário deletado')
    @api.response(400, 'Falha ao deletar usuário')
    def delete(self, user_id):
        """Deleta um usuário por ID"""
        try:
            success = UserService.delete_user(user_id)
            if success:
                return response(
                    status=204,
                    name_of_content='message',
                    content={},
                    message='Usuário deletado com sucesso'
                )
            else:
                return response(
                    status=404,
                    name_of_content='error',
                    content={},
                    message='Usuário não encontrado'
                )
        except Exception as e:
            return response(
                status=400,
                name_of_content='error',
                content={},
                message=str(e)
            )

@api.route('/login')
class UserLogin(Resource):
    @api.doc('login_user')
    @api.expect(login_model)
    @api.response(200, 'Login successful')
    @api.response(401, 'Invalid credentials')
    def post(self):
        """Authenticate a user"""
        data = request.get_json()
        print(request.method)
        cpf_or_nickname = data.get('cpf_or_nickname')
        password = data.get('password')

        if not cpf_or_nickname or not password:
            return response(
                status=400,
                name_of_content='error',
                content={},
                message='CPF/nickname and password are required'
            )

        user = UserService.authenticate_user(cpf_or_nickname, password)
        if user:
            return response(
                status=200,
                name_of_content='user',
                content={
                    'user_id': user.user_id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'nickname': user.nickname,
                    'cpf': user.cpf,
                    'phone_number': user.phone_number,
                    'profile_picture': user.profile_picture,
                    'quote': user.quote
                }
            )
        else:
            return response(
                status=401,
                name_of_content='error',
                content={},
                message='Invalid credentials'
            )