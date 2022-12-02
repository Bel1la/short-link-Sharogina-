from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager


import resources, server



app = Flask(__name__)
api = Api(app)

app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
jwt = JWTManager(app)


@app.route('/')
def index():
    return jsonify({'message': 'Hello, World!'})


# регистрация
api.add_resource(resources.UserRegistration, '/reg')
# авторизация
api.add_resource(resources.UserLogin, '/auth')
# создание ссылки
api.add_resource(resources.CreateShortLink, '/createLink')
# смена названия
api.add_resource(resources.changeNameLink,"/changeNick")
# получение всех ссылок пользователя
api.add_resource(resources.allUserLinks,"/getAllLinks")
# редирект
api.add_resource(resources.getLink,"/getLink")
# удаление ссылки
# смена доступа к ссылке
api.add_resource(resources.changePrivacyLink,"/changePrivacy")





api.add_resource(resources.prob, '/prob')
# app = create_app()
import datetime
now = datetime.datetime.now()

if __name__ == '__main__':
    server.createTables()
    print("hi",now.time())
    app.run(debug=True)

