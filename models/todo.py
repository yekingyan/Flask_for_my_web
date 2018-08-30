from models import Model
import time
from flask import request
from tools import (
    strftime,
    log,
)
from models.user import (
    current_user_name,
)
from models.mongodb import MongoDB


class Todo(MongoDB, Model):
    def __init__(self, form):
        self.id = None
        self.title = form.get('title', '')
        self.complete = False
        # 创建时间，更新时间
        self.ct = int(time.time())
        self.ut = self.ct
        self.cookie = request.cookies.get('cookie')
        self.user = None

    @classmethod
    def new(cls, form):
        """
        创建并保存一个todo,保存于Todo.txt
        :param form: todo字典,如{'title':'doing'}
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

        # 加入加户标记
        username = current_user_name()
        t.user = username

        return t

    @classmethod
    def update(cls, id, form):
        """更新todo"""
        t = cls.find(id)
        valid_names = [
            'title',
            'completed',
        ]
        for key in form:
            if key in valid_names:
                # 更新为form中的数据
                setattr(t, key, form[key])
        t.save()
        return t

    @classmethod
    def complete(cls, id, completed=True):
        """"""
        t = cls.find(id)
        t.complete = completed
        t.save()
        return t

    @classmethod
    def all_by_cookie(cls):
        """从所有todo中返回属于请求cookie的数据"""
        all_list = cls.all()
        data_by_cookie = []
        for l in all_list:
            if l.cookie == request.cookies.get('cookie'):
                # 时间格式转换
                l.ct = strftime(l.ct)
                data_by_cookie.append(l)
        return data_by_cookie

    @classmethod
    def id_for_cookie(cls, todo_id):
        """返回所在的id的cookie值"""
        models = cls.all()
        for m in models:
            # print(m)
            if m.id == todo_id:
                return m.cookie

    @staticmethod
    def user_in_todo(user):
        """
        传入用户对象
        为todo加入当前登陆用户属性
        """
        cookie = request.cookies.get('cookie')
        todos = Todo.find_all(cookie=cookie)
        log('user in todo', todos)
        if len(todos) >= 1:
            for t in todos:
                # 只有t.user为空时才能加入，
                # 避免重复注册导致数据迁移
                if t.user is None:
                    t.user = user.username
                    t.save()

    @classmethod
    def all_by_user(cls):
        """从所有todo中返回属于请求cookie的数据"""
        all_list = cls.all()
        data_by_cookie = []

        for l in all_list:
            if l.user == current_user_name():
                # 时间格式转换
                l.ct = strftime(l.ct)
                data_by_cookie.append(l)
        return data_by_cookie

    # @classmethod
    # def id_for_user(cls, username):
    #     """返回所在的id的cookie值"""
    #     models = cls.all()
    #     for m in models:
    #         # print(m)
    #         if m.username == username:
    #             return m.username

# if __name__ == '__main__':
#     print('text')