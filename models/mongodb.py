from pymongo import MongoClient

# 初始化 连接mongo,连接数据库'flask_web'
# 数据库中表名的命名用类名
client = MongoClient()
db = client['flask_web']


class MongoDB(object):
    __fields = [
        '_id',
        # （字段名，类型，值）
        ('id', int, -1),
        ('type', str, ''),
        ('deleted', bool, False),
        ('ct', int, 0),
        ('ut', int, 0),
    ]

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

    def save(self):
        """
        通过判断id。保存新数据，或更新旧数据
        fixme id
        """
        db[self.class_name()].save(self.__dict__)

    @classmethod
    def find_by(cls, **kwargs):
        """
        fixme 返回对象
        """
        print("使用了Mongo")
        mongo_data = db[cls.__name__].find(kwargs)
        list_ = list(mongo_data)
        m = cls({})
        for dict_ in list_:
            for k, v in dict_.items():
                setattr(m, k, v)
        return m


if __name__ == '__main__':
    db = client['web']
    l = list(db.Todo.find())
    for d in l:
        print(d)
    # print(l)
