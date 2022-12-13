from flask_restful import Resource
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, get_jwt_identity)
# get_raw_jwt    jwt_refresh_token_required,   flask--jsonify,
import server, hashlib, random
from flask import Flask, request, redirect,  make_response
from werkzeug.security import generate_password_hash, check_password_hash



# регистрация
class UserRegistration(Resource):
    def post(self):
        login = str(request.json.get("login", None))
        password = str(request.json.get("password", None))
        hash_pass = generate_password_hash(password)
        res = server.Registered(login, hash_pass)
        if res == True:
            return make_response(f"пользователь {login} зарегистрирован")
        else:
            return make_response(f'такой пользователь уже существует')


# авторизация
class UserLogin(Resource):
    def post(self):
        login = str(request.json.get("login", None))
        password = str(request.json.get("password", None))
        hash_pass = server.Autorized(login)
        access_token = create_access_token(identity=login)

        if check_password_hash(hash_pass, password) and hash_pass != None:
            return make_response(f"пользователь {login} вошел,\n токен: {access_token}")
        else:
            return make_response("неправильные логин или пароль")



# createLink создание ссылки
class CreateShortLink(Resource):
    @jwt_required()
    def get(self):
        link = str(request.json.get("link", None))
        if server.checkLinkforUser(get_jwt_identity(), link):
            sok = hashlib.md5(link.encode()).hexdigest()[:random.randint(8, 12)]
            server.addLink(get_jwt_identity(), link, sok)
            return make_response(sok)
        else:
            return make_response("у вас уже имеется сокращение данной ссылки")





# получение всех ссылок пользователя
class allUserLinks(Resource):
    @jwt_required()
    def get(self):
        login = get_jwt_identity()
        res=server.getAllUserLinks(login)
        return make_response(f"ваши ссылки: {res}")


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

# редирект публичной ссылки
class getPublicLink(Resource):
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

# редирект защищенной ссылки
class getNoPublicLink(Resource):
    @jwt_required()
    def get(self):
        user_id=server.foundUserId(get_jwt_identity())
        nick = str(request.json.get('nick', None))
        res=server.getProtectedLink(nick)
        # print(res)
        if user_id==res[1] and res[2]==3:
            return redirect(res[0])
        # (user_id!=res[1] or user_id==res[1]) and
        elif res[2]==2 or res[2]==1:
            return redirect(res[0])
        else:
            return make_response("у вас нет доступа к этой ссылке")




        # return redirect(res, code=302)
# удалить ссылку
class deleteLink(Resource):
    @jwt_required()
    def get(self):
        login=get_jwt_identity()
        nick = str(request.json.get('nick', None))
        if(server.foundLink(nick))and server.deleteLink(login,nick):

            return make_response("ссылка была удалена")
        else:
            return make_response("такой ссылки нет или вы не имеете доступа к ней")

