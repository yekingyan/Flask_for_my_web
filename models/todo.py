from models import Model
import time
from flask import request
from models.user import get_cookie


class Todo(Model):
    def __init__(self, form):
        self.id = None
        self.title = form.get('title', '')
        self.completed = False
        # 创建时间，更新时间
        self.ct = int(time.time())
        self.ut = self.ct
        self.cookie = request.cookies.get('cookie')

    @classmethod
    def new(cls, form):
        """
        创建并保存一个todo
        :param form: todo字典,如{'title':'doing'}
        :return: todo实例
        """
        t = cls(form)
        t.save()
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
            if l.cookie == get_cookie():
                data_by_cookie.append(l)
        return data_by_cookie