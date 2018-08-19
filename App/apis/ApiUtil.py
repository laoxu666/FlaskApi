# 只要可以进入这个文件 证明已经登录了


from flask import request, g
from flask_restful import Resource

from App.ext import cache
from App.models import User

# 权限设计  封装一下
# 小说列表只有登录才能看   小说详情只有会员能看

# &&&&&&&&& 这样做法还是不够优秀，最好使用装饰器ApiDecorator.py  &&&&&&&&&&&&&&&&&&&&&&&


class BaseResource(Resource):

    def get(self):

        token = request.args.get('token')

        if token:

            u_id = cache.get(token)

            if u_id:
                user = User.query.get(u_id)

                if user:

                    if not user.is_delete:

                        g.user = user

                        return self.get_data()

                    else:
                        data = {
                            'msg': 'user deleted'
                        }
                        return data

                else:
                    data = {
                        'msg': 'user not exist'
                    }
                    return data

            else:
                data = {
                    'msg': 'user not avalibal'
                }
                return data

        else:
            data = {
                'msg': 'user not login'
            }
            return data

    def get_data(self):

        raise NotImplementedError()
