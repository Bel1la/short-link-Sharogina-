from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, get_jwt_identity)
# get_raw_jwt    jwt_refresh_token_required,
import server, hashlib, random
from flask import Flask, request, redirect, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash


# parser = reqparse.RequestParser()

# регистрация
class UserRegistration(Resource):
    def post(self):
        # parser = reqparse.RequestParser()
        # parser.add_argument('login', help='Пустое поле имени', required=True)
        # parser.add_argument('password', help='Пустое поле пароля', required=True)
        # reqparse.RequestParser(login,password)
        # data = parser.parse_args()

        login = str(request.json.get("login", None))
        password = str(request.json.get("password", None))
        hash_pass = generate_password_hash(password)
        res = server.Registered(login, hash_pass)
        if res == True:
            access_token = create_access_token(identity=login)
            refresh_token = create_refresh_token(identity=login)
            return {
                'message': 'пользователь {} зарегистрирован'.format(login),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        else:
            return {'message': 'такой пользователь уже существует'}


# авторизация
class UserLogin(Resource):
    def post(self):
        # parser = reqparse.RequestParser()
        # parser.add_argument('login', help='Пустое поле имени', required=True)
        # parser.add_argument('password', help='Пустое поле пароля', required=True)
        # data = parser.parse_args()

        # login = data['login']
        login = str(request.json.get("login", None))
        # password = data['password']
        password = str(request.json.get("password", None))
        hash_pass = server.Autorized(login)

        if check_password_hash(hash_pass, password) and hash_pass != None:
            access_token = create_access_token(identity=login)
            # refresh_token = create_refresh_token(identity=data['login'])
            return {
                'message': 'пользователь {} вошел'.format(login),
                'access_token': access_token,
                # 'refresh_token': refresh_token
            }
        else:
            return {
                'message': 'неправильные логин или пароль'}


# return data
# return {'message': 'User login'}

# createLink создание ссылки
class CreateShortLink(Resource):
    @jwt_required()
    def get(self):
        # parser = reqparse.RequestParser()
        # parser.add_argument('link', help='Пустое поле ', required=True)
        # data = parser.parse_args()

        link = str(request.json.get("link", None))
        # link = data['link']
        if server.checkLinkforUser(get_jwt_identity(), link):
            sok = hashlib.md5(link.encode()).hexdigest()[:random.randint(8, 12)]
            server.addLink(get_jwt_identity(), link, sok)
            return {
                'message': sok
            }
        else:
            return {
                'message': "у вас уже имеется сокращение данной ссылки"
            }




# получение всех ссылок пользователя
class allUserLinks(Resource):
    @jwt_required()
    def get(self):
        login = get_jwt_identity()
        res=server.getAllUserLinks(login)
        # print(res.)
        return make_response(f"ваши ссылки: {res}")
#     ' '.join(res)


# смена названия
class changeNameLink(Resource):
    @jwt_required()
    def get(self):
        old = str(request.json.get('old_nick', None))
        new = str(request.json.get('new_nick', None))
        login = get_jwt_identity()
        if server.changeNameLink(login, old, new):
            return make_response(["название ссылки c ", old, " изменено на", new])
        else:
            return make_response("название не изменено, такой ссылки нет")


# смена доступа к ссылке
class changePrivacyLink(Resource):
    @jwt_required()
    def get(self):
        nick = str(request.json.get('nick', None))
        privacy = str(request.json.get('privacy', None))
        login = get_jwt_identity()
        if server.changePrivacyLink(login, nick, privacy):
            return make_response("доступ был изменен ")
        else:
            return make_response("доступ не изменен, такой ссылки нет")

# редирект
class getLink(Resource):
    def get(self):
        nick = str(request.json.get('nick', None))
        res=server.getPublicLink(nick)
        if server.foundLink(nick):
            if res!=False:
                return redirect(res)
            else:
                return make_response("у вас нет доступа к этой ссылке, войдите в аккаунт")
        else:
            return make_response("такая ссылка не существует")


        # return redirect(res, code=302)







class prob(Resource):
    @jwt_required()
    def get(self):
        return {
            'message': get_jwt_identity()
        }
# class UserLogoutAccess(Resource):
#     def post(self):
#         return {'message': 'User logout'}
#
#
# class UserLogoutRefresh(Resource):
#     def post(self):
#         return {'message': 'User logout'}
#
#
# class TokenRefresh(Resource):
#     def post(self):
#         return {'message': 'Token refresh'}
#
#
# class AllUsers(Resource):
#     def get(self):
#         return {'message': 'List of users'}
#
#     def delete(self):
#         return {'message': 'Delete all users'}
#
#
# class SecretResource(Resource):
#     def get(self):
#         return {
#             'answer': 42
#         }
