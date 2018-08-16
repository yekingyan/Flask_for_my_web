from flask import (
    Flask,
    request,
    render_template,
)
from flask_bootstrap import Bootstrap


# 同级目录routes文件夹下todo.py
from routes.todo import main as todo
# 实例化Flask
app = Flask(__name__)
# 注册蓝图，url_prefix为每个main蓝图路由加上前缀
app.register_blueprint(todo, url_prefix='/todo')

bootstrap = Bootstrap(app)

@app.route('/')
def hello_world():
    return render_template('base2.html')


if __name__ == '__main__':
    config = dict(
        host="0.0.0.0",
        port=2000,
        debug=True,
    )
    app.run(host="0.0.0.0", port=2000)
