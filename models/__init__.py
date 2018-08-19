import json
from tools import log
from models.user import get_cookie


def save_for_json(data, path):
    """
    保存数据为json格式,写入文件
    :param data: 数据
    :param path: 存放路径
    """
    s = json.dumps(data, indent=2, ensure_ascii=False)
    # w 只写模式
    with open(path, 'w+', encoding='utf-8') as f:
        f.write(s)


def load_json(path):
    """
    解码json,读出文件
    :param path:
    :return: 解码的json数据
    """
    with open(path, 'r', encoding='utf-8') as f:
        s_json = f.read()
        log("f.read", s_json)
        s = json.loads(s_json)
        return s


class Model(object):
    """基类"""
    @classmethod
    def db_path(cls):
        """
        以类的名字保存txt文档，在/data
        :return: 如/data/todo.txt
        """
        class_name = cls.__name__
        path = f'data/{class_name}.txt'
        return path

    @classmethod
    def _new_form_dict(cls, d):
        """
        化字典为变量与属性值，初始化数据
        :param d: 字典
        :return: k = v
        """
        m = cls({})
        for k, v in d.items():
            # 将字典d的键值对放进m
            # m.k == v
            setattr(m, k, v)
        return m

    @classmethod
    def all(cls):
        """
        得到类对象所有的models
        :return: k = v
        """
        # 将该类对象data加载到models
        path = cls.db_path()
        log("path in all:", path)
        models = load_json(path)
        # 得到所有的得到所有的 models
        ms = [cls._new_form_dict(m) for m in models]
        log("ms", type(ms), ms)
        return ms

    @classmethod
    def find_all(cls, **kwargs):
        """
        :param kwargs: 比较的数据
        :return: 含属性值的对象m
        """
        ms = []
        log('kwargs:', kwargs, type(kwargs))
        k, v = '', ''
        for key, value in kwargs.items():
            k, v = key, value
        alls = cls.all()
        # 比较类对象数据是否与获取数据一致
        for m in alls:
            if v == getattr(m, k):
                ms.append(m)
        return ms

    @classmethod
    def find_by(cls, **kwargs):
        """
        kwargs是只有一个元素的dict
        u = User.find_by(username='sb')
        """
        log('kwargs: ', kwargs, type(kwargs))
        k, v = '', ''
        for key, value in kwargs.items():
            k, v = key, value
        alls = cls.all()
        for m in alls:
            if v == getattr(m, k):
                return m
        return None

    @classmethod
    def find(cls, id):
        return cls.find_by(id=id)

    @classmethod
    def delete(cls, id):
        """删除id指定的元素，并返回该元素"""
        models = cls.all()
        index = -1
        for i, e in enumerate(models):
            if e.id == id:
                index = i
                break
        # 如果没找到id
        if index == -1:
            pass
        else:
            obj = models.pop(index)
            l = [m.__dict__ for m in models]
            path = cls.db_path()
            save_for_json(l, path)
            return obj

    def __repr__(self):
        """打印字典对象的 string 格式"""
        class_name = self.__class__.__name__
        properties = [f'{k}: ({v})' for k, v in self.__dict__.items()]
        # 将列表转成字符串，换行
        s = '\n'.join(properties)
        return f'< {class_name}\n{s} \n>\n'

    def json(self):
        """返回当前model的字典表示"""
        # copy 会复制一份新数据并返回
        d = self.__dict__.copy()
        return d

    def save(self):
        """

        """
        models = self.all()
        # 如果没有id,说明是新元素
        if self.id is None:
            # 如果是空list
            if len(models) == 0:
                # 设置id为1
                self.id = 1
            else:
                # 是list最后的对象
                m = models[-1]
                self.id = m.id + 1
            models.append(self)
        else:
            index = -1
            for i, m in enumerate(models):
                if m.id == self.id:
                    index = i
                    break
            log("index in save", index)
            models[index] = self
        l = [m.__dict__ for m in models]
        path = self.db_path()
        save_for_json(l, path)