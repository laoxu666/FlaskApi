from flask_restful import Resource


class Hello(Resource):
    def get(self):
        return {"msg": 'Hello get'}

    def post(self):
        return {"msg": 'Hello post'}

    def delete(self):
        return {"msg": 'Hello delete'}

    def put(self):
        return {"msg": 'Hello put'}