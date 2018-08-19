from flask import request, g
from flask_restful import Resource

from App.apis.ApiDecorator import login_required, check_permission
from App.models.UserModel import WRITE, READ


class CodeResource(Resource):

    @login_required
    def get(self):
        # 只要能进到这， 意味着用户已经登录，并且是合法用户
        user = g.user

        data = {
            "status": 200,
            "msg": "user login ok",
            "u_name": user.u_name
        }
        return data

    # 判断是否有读权限
    @check_permission(READ)
    def post(self):
        data = {
            "status": 201,
            "msg": "read ok"
        }
        return data