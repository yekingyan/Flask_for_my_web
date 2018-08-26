from models import Model
import time
from flask import request
from tools import strftime


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
    def new_without_save(cls, form):
        t = cls(form)
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