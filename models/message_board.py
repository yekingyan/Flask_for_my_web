from models import Model
from models.mongodb import MongoDB
import time
from flask import (
    request,
    flash,
)
from models.user import (
    current_user_name,
    User,
)
from tools import (
    strftime,
    log,
)


class MessageBoard(MongoDB, Model):
    def __init__(self, form):
        self.id = None
        self.content = form.get('content', '')
        self.ct = int(time.time())
        self.ut = self.ct
        self.cookie = request.cookies.get('cookie')
        self.message_user = form.get('user', '')
        self.user = None
        self.delete = False

    @classmethod
    def new_without_save(cls, form):
        """
        将表单数据传入类，
        在__init__()变成类属性
        """
        t = cls(form)

        # 加入加户标记
        username = current_user_name()
        t.user = username
        return t

    @classmethod
    def all_user(cls):
        """返回所有用户的用户，包含Message库与User库"""
        # 非注册用户
        all_list = cls.all()
        data_by_message_user = [c.message_user for c in all_list]
        # 注册同户
        register_list = User.all()
        register = [u.username for u in register_list]
        all_user_list = data_by_message_user + register
        return all_user_list

    @classmethod
    def all_message(cls):
        """返回所留言数据"""
        all_list = cls.all()
        data = []
        # 转换时间格式
        for l in all_list:
            if l.delete is False:
                l.ct = strftime(l.ct)
                data.append(l)
        return data

    @classmethod
    def delete(cls, id):
        print('delete', id)
        m = MongoDB.find_by(id=int(id))
        if current_user_name() == m.user:
            m.delete = True
            m.save()
            log(f'{m.user}\n删除了\n{m.content}')
        elif request.cookies.get('cookie') == m.cookie:
            m.delete = True
            m.save()
            log(f'{m.cookie}\n删除了\n{m.content}')
        else:
            flash("你不能删除别人的内容，或你的身份已经过期")