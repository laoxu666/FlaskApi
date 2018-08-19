import hashlib

from werkzeug.security import generate_password_hash, check_password_hash

from App.ext import db
from App.models.ModelUtil import BaseModel


class User(BaseModel, db.Model):
    u_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    u_name = db.Column(db.String(32), unique=True)
    _u_password = db.Column(db.String(256))
    is_delete = db.Column(db.Boolean, default=False)
    u_permission = db.Column(db.Integer, default=0)

    """
    # ********************* 密码安全 方式一 md5  封装一下 *************************** 1
    def set_password(self, password):
        md5 = hashlib.md5()                 # md5  默认128位 二进制 可以转换成 uncode 码
        md5.update(password.encode("utf8"))
        password = md5.hexdigest()
        self.u_password = password

    # 验证密码
    def verify_password(self, password):
        md5 = hashlib.md5()
        md5.update(password.encode("utf8"))
        password = md5.hexdigest()
        return self.u_password == password
    """

    """
    # ********************* 密码安全 方式一 md5  封装一下 *************************** 2
    def set_password(self, password):
        password = self._to_hash(password)
        self.u_password = password

    # 验证密码
    def verify_password(self, password):
        password = self._to_hash(password)
        return self.u_password == password

    
    # hash 操作封装一下   方式一   这个方式还不算优秀换一种  generate_password_hash
    def _to_hash(self, password):
        md5 = hashlib.sha512()
        md5.update(password.encode("utf8"))
        return md5.hexdigest()
    """

    """
    # ************ 密码安全 方式二 generate_password_hash 相对好一些 *************** 3
    # 密码安全操作
    def set_password(self, password):
        password = self._to_hash(password)
        self.u_password = password

    # 验证密码
    def verify_password(self, password):
        password = self._to_hash(password)
        return check_password_hash(self.u_password, password)

    def _to_hash(self, password):
        return generate_password_hash(password)
    """

    # ************ 密码安全 方式三 最优秀设计方法 *************** 4  最终选择
    @property
    def u_password(self):
        return self._u_password

    @u_password.setter
    def u_password(self, password):
        self._u_password = generate_password_hash(password)

    # 验证密码
    def verify_password(self, password):
        return check_password_hash(self._u_password, password)