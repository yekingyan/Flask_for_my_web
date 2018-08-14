from models import Model
import time


class Todo(Model):
    def __init__(self, form):
        self.id = None
        self.title = form.get('title', '')
        self.completed = False
        # 创建时间，更新时间
        self.ct = int(time.time())
        self.ut = self.ct

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
        """Todo.complete(1)删，False则恢愎"""
        t = cls.find(id)
        t.complete = completed
        t.save()
        return t

