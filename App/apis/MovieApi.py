from flask_restful import Resource, reqparse, fields, marshal_with
from App.models.MovieModel import Movie

# 输出参数
parser = reqparse.RequestParser()
parser.add_argument("movie_name", type=str, help="")
parser.add_argument("movie_tyepe", required=False)  # 参数是否必须加
parser.add_argument("hobby", action="append")  # 参数追加  一个key 对应多个value
parser.add_argument("csrftoken", location="cookies")  # location 位置

movie_fields = {
    'm_name': fields.String
}

# 输出数据格式化
response_movie_fields = {
    # 'msg': fields.String,
    'message': fields.String(attribute="msg"),  # attribute 修改属性名
    'status': fields.Integer(default=666),  # default  设置默认值
    "data": fields.Nested(movie_fields)
}

response_movies_fields = {
    'msg': fields.String,
    'status': fields.Integer,
    "data": fields.List(fields.Nested(movie_fields))
}


# 单个数据操作
class MovieResource(Resource):
    @marshal_with(response_movie_fields)
    def get(self, id=0):  # 根据 id 获取单个数据
        movie = Movie.query.get(id)
        data = {
            'status': 201,
            'msg': 'ok',
            'data': movie
        }
        return data

    # 修改单个电影数据操作
    @marshal_with(response_movie_fields)
    def post(self, id=0):
        args = parser.parse_args()
        movie_id = id
        movie = Movie.query.get(movie_id)
        movie_name = args.get("movie_name")
        movie.m_name = movie_name
        movie.save()
        data = {
            'status': 200,
            "msg": 'ok',
            'data': movie
        }
        return data

    # 删除单个数据
    def delete(self, id=0):
        movie_id = id
        movie = Movie.query.get(movie_id)
        movie.delete()
        data = {
            'status': 204,
            'msg': 'delete ok'
        }
        return data


# 多个数据操作
class MoviesResource(Resource):
    @marshal_with(response_movies_fields)
    def get(self):
        movies = Movie.query.all()
        data = {
            'status': 201,
            'msg': 'ok',
            'data': movies
        }
        return data

    # 创建电影数据操作
    @marshal_with(response_movie_fields)
    def post(self):
        args = parser.parse_args()
        movie_name = args.get("movie_name")
        movie = Movie()
        movie.m_name = movie_name

        if movie.save():
            data = {
                'status': 200,
                'msg': 'ok',
                'data': movie
            }
            return data
        else:
            data = {
                'status': 400,
                'msg': 'create fail'
            }
            return data
