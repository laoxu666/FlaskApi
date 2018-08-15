from flask_restful import Api

from App.apis.HelloApi import Hello

api = Api()


def init_api(app):
    api.init_app(app=app)


api.add_resource(Hello, '/hello/')