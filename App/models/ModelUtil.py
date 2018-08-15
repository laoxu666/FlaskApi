from flask_restful import abort

from App.ext import db


class BaseModel:

    # save 创建保存数据方法
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            print("error:", e)
            return False

    # save 创建保存数据方法
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            print("error:", e)
            return False