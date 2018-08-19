from flask import request, g
from flask_restful import abort

from App.ext import cache
from App.models import User


# 封装函数 判断用户是否登录
# 使用装饰器
def login_required(fun):

    def wrapper(*args, **kwargs):

        token = request.args.get("token")

        if token:

            u_id = cache.get(token)

            if u_id:

                user = User.query.get(u_id)

                if user:

                    if not user.is_delete:

                        g.user = user

                        return fun(*args, **kwargs)

                    else:
                        abort(403, message="user deleted")
                else:
                    abort(400, message="user not exist")
            else:
                abort(401, message="user not available")

        else:
            abort(401, message="user not login")
    return wrapper


# def check_permission(permission):
#
#     def wrapper_outer(fun):
#
#         def wrapper(*args, **kwargs):
#
#             token = request.args.get("token")
#
#             if token:
#
#                 u_id = cache.get(token)
#
#                 if u_id:
#
#                     user = User.query.get(u_id)
#
#                     if user:
#
#                         if not user.is_delete:
#
#                             if user.check_permission(permission):
#
#                                 g.user = user
#
#                                 return fun(*args, **kwargs)
#                             else:
#                                 abort(403, message="can not access")
#                         else:
#                             abort(403, message="user deleted")
#                     else:
#                         abort(400, message="user not exist")
#                 else:
#                     abort(401, message="user not available")
#
#             else:
#                 abort(401, message="user not login")
#         return wrapper
#     return wrapper_outer

# 权限封装
def check_permission(permission):

    def wrapper_outer(fun):

        def wrapper(*args, **kwargs):

            token = request.args.get("token")

            if not token:
                abort(401, message="user not login")

            u_id = cache.get(token)

            if not u_id:
                abort(401, message="user not available")

            user = User.query.get(u_id)

            if not user:
                abort(400, message="user not exist")

            if user.is_delete:
                abort(403, message="user deleted")

            if not user.check_permission(permission):
                abort(403, message="can not access")

            g.user = user

            return fun(*args, **kwargs)
        return wrapper
    return wrapper_outer