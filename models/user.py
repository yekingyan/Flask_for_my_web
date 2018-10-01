import string
import random
from flask import request, session, make_response
from models import Model
import time
import hashlib
from tools import log
from models.mongodb import MongoDB


def salt():
    """
    返回16位随机字符串
    """
    # 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    str_ascii = string.ascii_letters
    # '0123456789'
    str_digits = string.digits
    # '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    str_punctuation = string.punctuation

    mix_str = str_ascii + str_digits + str_punctuation

    salt16 = ''.join(random.sample(mix_str, 16))
    return salt16


def current_user():
    """通过session的user_id返回用户对象"""
    user_id = session.get('user_id')
    user = User.find_by(id=user_id)
    return user


def current_user_name():
    """获取当前用户的用户名"""
    u = current_user()
    if u is not None:
        username = u.username
    else:
        username = None
    return username


def set_salt_cookie(template):
    r = make_response(template)
    if request.cookies.get('cookie') is None:
        r.set_cookie('cookie', salt(), max_age=2419200)
    return r


class User(MongoDB, Model):
    def __init__(self, form):
        self.username = form.get('username')
        self.password = form.get('password')
        self.id = None
        # 创建时间，更新时间
        self.ct = int(time.time())
        self.cookie = request.cookies.get('cookie')

    @classmethod
    def new(cls, form):
        """
        创建并保存一个user,保存于User.txt
        :param form: user字典,如{'username':'bob', "password":'123'}
        :return: todo实例
        """
        t = cls(form)
        t.save()
        return t

    @classmethod
    def new_without_save(cls, form):
        """
        将表单数据传入Todo类，
        在__init__()变成类属性
        """
        t = cls(form)
        return t

    @staticmethod
    def hashed_password_salt(pwd):
        """将密码加盐，返回hashed值"""
        ascii_pwd = pwd.encode('ascii')
        salts = "h{GWUoQ12(@B5c+#1N7Rz0uq)SB;{i=k"
        ascii_salt = salts.encode('ascii')
        hashed = hashlib.sha256(ascii_pwd + ascii_salt).hexdigest()
        return hashed

    @classmethod
    def add_new_user(cls, form):
        """
        增加新注册用户入数据库
        如果有重名，返回字符串"重名"
        如果用户名或密码格式不对，返回"用户名或密码太短了"
        """
        username = form.get('username')
        password = form.get('password')

        # 验证是否有重名
        alls = User.all()
        for l in alls:
            if l.username == username:
                return '重名'

        # 验证密码与用户名格式
        if len(username) <= 2 or len(password) <= 2 or len(username) > 8:
            return "用户名或密码太短了"
        else:
            # 创建对象u，设置属性
            u = User.new_without_save(form)
            # log('before hashed', u.password)
            u.password = User.hashed_password_salt(password)
            # log('hashed', u.password)
            # 保存入User.txt
            u.save()
            return u

    @classmethod
    def verify_user(cls, form):
        """验证用户名或密码是否一致"""
        username = form.get('username')
        password = form.get('password')
        # log("v u p", username, password)
        u = cls.find_by(username=username)
        # log('uu', u)
        if u is not None and u.password == User.hashed_password_salt(password):
            return u
        else:
            return None

    @staticmethod
    def multi_add_user():
        """通过cookie追踪用户是重复注册,写入log.txt"""
        cookie = request.cookies.get('cookie')
        old_u = User.find_by(cookie=cookie)
        if old_u is not None:
            log(f"{old_u.username}在重复注册")

# if __name__ == '__main__':
# print(hashed_password_salt('aaa'))
# print(salt())
#
