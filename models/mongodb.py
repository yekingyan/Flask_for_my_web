from pymongo import MongoClient
from tools import log

# 初始化 连接mongo,连接数据库'flask_web'
# 数据库中表名的命名用类名
client = MongoClient()
db = client['flask_web']


class MongoDB(object):

    def class_name(self):
        """返回类的名字"""
        name = self.__class__.__name__
        return name

    def __repr__(self):
        class_name = self.__class__.__name__
        contents = (f'{k} = {v}' for k, v in self.__dict__.items())
        str_contents = '\n    '.join(contents)
        class_contents = f"<{class_name}: \n  {str_contents}\n>"
        return class_contents

    @classmethod
    def _find(cls, **kwargs):
        """
        有条件的查找，返回生成器
        """
        yield_ = db[cls.__name__].find(kwargs)
        return yield_

    @classmethod
    def _delete(cls, **kwargs):
        db[cls.__name__].find_one_and_delete(kwargs)

    @classmethod
    def _insert_one(cls, **kwargs):
        db[cls.__name__].insert_one(kwargs)

    @classmethod
    def _replace_one(cls, **kwargs):
        # fixme replace_one(d1, d2) d1更替为d2
        db[cls.__name__].replace_one(kwargs)

    @classmethod
    def _new_form_dict(cls, d):
        """
        化字典为对象（变量与属性值），初始化数据
        :param d: 字典
        :return: m对象   m.key == value
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
        得到该类所有的对象,以列表的形式返回
        """
        yield_ = cls._find()
        ms = [cls._new_form_dict(m) for m in yield_]
        return ms

    def save(self):
        """
        通过判断id。保存新数据，或更新旧数据
        fixme id user
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

        # 找到对象列表的索引，更改为新的数据
        else:
            index = -1
            for i, m in enumerate(models):
                if m.id == self.id:
                    index = i
                    break
            # log("index in save", index)
            models[index] = self
        for m in models:
            db[self.class_name()].save(m.__dict__)

    @classmethod
    def find_by(cls, **kwargs):
        """
        输入键值对，返回所属的对象
        用法: u = User.find_by(username='sb')
        """
        mongo_data = db[cls.__name__].find(kwargs)
        list_ = list(mongo_data)
        # print('mongo', list_)
        # print(kwargs)
        m = cls({})
        for dict_ in list_:
            for k, v in dict_.items():
                setattr(m, k, v)
        # print('mongo m', m)
        return m

    @classmethod
    def delete(cls, id):
        """
        通过id删除mongodb中的数据
        返回被删的对象
        """
        obj = cls._find(id=id)
        cls._delete(id=id)
        return obj


if __name__ == '__main__':
    db = client['flask_web']
    query = {
        "id": 15,
        "title": "save的测试",
        "complete": False,
        "ct": 1535634493,
        "ut": 1535634493,
        "cookie": "HgAbUo0ZxmJchuI5",
        "user": None,
    }
    lq = (db.Todo.find())
    for d in lq:
        print(d)
    # print(list(lq))
