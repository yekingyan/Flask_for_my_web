from flask import (
    Flask,
    request,
)

# 同级目录routes文件夹下todo.py
from routes.todo import main as todo
# 实例化Flask
app = Flask(__name__)
# 注册蓝图，url_prefix为每个main蓝图路由加上前缀
app.register_blueprint(todo, url_prefix='/todo')


@app.route('/')
def hello_world():
    a = request.method
    return '<h1>Hello World!</h1>'


if __name__ == '__main__':
    config = dict(
        host="0.0.0.0",
        port=2000,
        debug=True,
    )
    app.run(host="0.0.0.0", port=2000)
