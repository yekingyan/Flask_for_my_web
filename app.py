from flask import (
    Flask,
    request,
    render_template,
    make_response,
    session,
)
from flask_bootstrap import Bootstrap
from models.user import (
    salt,
    current_user,
    current_user_name,
)
from routes.user import main as user
# 同级目录routes文件夹下todo.py
from routes.todo import main as todo


# 实例化Flask
app = Flask(__name__)

# 注册蓝图，url_prefix为每个main蓝图路由加上前缀
app.register_blueprint(todo, url_prefix='/todo')
app.register_blueprint(user)

bootstrap = Bootstrap(app)

app.secret_key = 'asdkjfhsiw@#sf64461dasf#$%'


@app.route('/')
def index():
    username = current_user_name()
    template = render_template('index.html', username=username)
    r = make_response(template)
    if request.cookies.get('cookie') is None:
        r.set_cookie('cookie', salt(), max_age=2419200)
    return r


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


if __name__ == '__main__':
    config = dict(
        host="0.0.0.0",
        port=2000,
        debug=True,
    )
    app.run(**config)
