from flask_restful import Api


from App.apis.HelloApi import Hello
from App.apis.MovieApi import MovieResource, MoviesResource

api = Api()


def init_api(app):
    api.init_app(app=app)


api.add_resource(Hello, '/hello/')
api.add_resource(MoviesResource, '/movies/')
api.add_resource(MovieResource, '/movies/<int:id>/')