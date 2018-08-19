# 权限设计
# 小说列表只有登录才能看   小说详情只有会员能看
from flask import g

from App.apis.ApiUtil import BaseResource


class BookResource(BaseResource):
    def get_data(self):

        user = g.user

        data = {
            'status': 200,
            'msg': '666',
            'u_name': user.u_name
        }

        return data

