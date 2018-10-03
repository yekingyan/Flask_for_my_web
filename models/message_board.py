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
import json
import urllib.request
import os


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
    def all_msg_include_del(cls):
        ms = cls.all()
        return ms

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
        m = cls.find_by(id=int(id))
        if current_user_name() == m.user and current_user_name() is not None:
            # print("wtffffffffff", current_user_name(), m.user)
            m.delete = True
            m.save()
            log(f'{m.user} 删除了\n{m.content}')
        elif request.cookies.get('cookie') == m.cookie and m.user is None:
            # # _________________________
            # print(request.cookies.get('cookie'))
            # print(m.cookie)
            m.delete = True
            m.save()
            log(f'{m.cookie} 删除了\n{m.content}')
        else:
            flash("你不能删除别人的内容，或你的身份已经过期")
            return {'flash': '你不能删除别人的内容，或你的身份已经过期'}
        return m


def guest(form):
    m = MessageBoard.new_without_save(form)
    # 第一次之后就不用输临时用户名，则m.message为空,此时要指定旧数据中的用户名给它
    if m.message_user is '':
        m.message_user = MessageBoard.find_by(cookie=request.cookies.get('cookie')).message_user
    # print(m.content, type(m.content), len(m.content))
    # if m.content != ' ' and len(m.content) != 0:
    #     m.save()
    # 用于第一次输入临时用户名找到是否存在cookie，有值就表名用户名重复了
    check_cookie = MessageBoard.find_by(message_user=m.message_user).cookie
    return m, check_cookie


class CityCode(object):
    _city_code = None

    def __new__(cls):
        if cls._city_code is None:
            path = os.path.join(os.getcwd(), 'data', 'city')
            with open(path, 'r', encoding='utf-8') as f:
                d = json.load(f)
                cls._city_code = d
        return cls._city_code

    @classmethod
    def city_to_code(cls, addr):
        city = addr['city_addr']
        code = cls._city_code[city]
        return code

    @staticmethod
    def get_weather_data(url):
        response = urllib.request.urlopen(url)
        r = response.read().decode('utf-8')
        d = json.loads(r)['value'][0]
        g = d['indexes'][2]
        w = d["weathers"][0]
        pm25 = {
            "aqi": d['pm25']['aqi'],
            'cityrank': d['pm25']['cityrank'],
            'pm10': d['pm25']['pm10'],
            'pm25': d['pm25']['pm25'],
            'quality': d['pm25']['quality'],
        }
        gm = {'content': g['content']}
        weather = {
            'temp_day_c': w['temp_day_c'],
            "temp_night_c": w["temp_night_c"],
            'weather': w['weather'],
        }
        data = {
            'pm25': pm25,
            'gm': gm,
            'weather': weather,
        }
        return data
