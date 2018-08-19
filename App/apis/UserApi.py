import uuid

from flask_restful import Resource, reqparse, fields, marshal, marshal_with

from App.ext import cache
from App.models import User


# 输出参数
parser = reqparse.RequestParser()
parser.add_argument('u_name', required=True, help="请输入用户名")
parser.add_argument('u_password', required=True, help="请输入密码")

# 比较常见的位置直接放在   ?action=login, register
parser.add_argument('action', required=True, help="请提供具体操作")

# 内层参数格式化
user_fields = {
    'u_name': fields.String,
    'u_permission': fields.Integer,
}

# 外层输出参数格式化
response_user_fields = {
    'status': fields.Integer,
    'msg': fields.String,
    'data': fields.Nested(user_fields)
}


# 外层输出参数格式化  + token
response_user_token_fields = {
    'status': fields.Integer,
    'msg': fields.String,
    'token': fields.String,
    'data': fields.Nested(user_fields)
}


# 用户注册登录 操作  其中密码做了数据安全
class UsersResource(Resource):
    # @marshal_with(response_user_fields)  # 加装饰器和不加装饰器 两种方式都行
    def post(self):

        args = parser.parse_args()

        action = args.get("action")
        u_name = args.get("u_name")
        u_password = args.get("u_password")

        data = {
            "status": 201,
            "msg": 'ok',
        }

        if action == "login":       # 用户登录

            user = User.query.filter(User.u_name.__eq__(u_name)).one_or_none()

            if user:

                if not user.verify_password(u_password):
                    data['status'] = 406
                    data['msg'] = 'password fail'
                    return data

                elif user.is_delete:
                    data['status'] = 900
                    data['msg'] = 'user is deleted'
                    return data

                else:
                    data['data'] = user

                    token = str(uuid.uuid4())    # token 需要转换为字符串

                    # 将用户token 存到缓存中 可以根据token 找到用户id 也可以根据用户id 找到token
                    # key: 使用token  值:用户id
                    cache.set(token, user.u_id, timeout=60*60*24*7)

                    data['token'] = token

                    return marshal(data, response_user_token_fields)

            else:
                data['status'] = 406
                data['msg'] = 'user not exist'
                return data

        elif action == "register":   # 用户注册

            user = User()

            user.u_name = u_name

            # 密码做数据安全处理
            # user.set_password(u_password)

            # 最终方法  密码做数据安全处理
            user.u_password = u_password

            user.save()

        data['data'] = user
        return marshal(data, response_user_fields)
        # return data


# 更新用户信息不更改用户名，只改密码
parser_user = reqparse.RequestParser()
parser_user.add_argument('u_password', required=True, help='请输入新密码')


# 单个用户数据操作  查询 修改 删除
class UserResource(Resource):
    # 根据 id 获取用户信息
    @marshal_with(response_user_fields)
    def get(self, id):

        user = User.query.get(id)

        data = {
            "status": 200,
            "msg": 'ok',
            'data': user,
        }
        return data

    # 根据 id 修改用户信息 --> 密码修改
    @marshal_with(response_user_fields)
    def post(self, id):

        args = parser_user.parse_args()

        u_password = args.get("u_password")

        user = User.query.get(id)

        user.u_password = u_password

        user.save()

        data = {
            "status": 200,
            "msg": 'password change ok',
            'data': user,
        }
        return data

    # 根据 id 删除某个用户   Model中应该设计一个字段 is_delete 来判断是否已删除
    @marshal_with(response_user_fields)
    def delete(self, id):

        user = User.query.get(id)

        user.is_delete = True       # is_delete = 1  表示删除用户

        user.save()

        data = {
            "status": 200,
            "msg": 'delete ok',
            "data": user,
        }
        return data