from flask import (
    Flask,
    request,
    render_template,
    redirect,
)
from flask_bootstrap import Bootstrap
from models.user import (
    current_user_name,
    set_salt_cookie,
)
from routes.user import main as user
# 同级目录routes文件夹下todo.py
from routes.todo import main as todo
from routes.video import main as video
from routes.message_board import main as message, socketio
from tools import log


# 实例化Flask
app = Flask(__name__)

# 注册蓝图，url_prefix为每个main蓝图路由加上前缀
app.register_blueprint(todo, url_prefix='/todo')
app.register_blueprint(user)
app.register_blueprint(message, url_prefix='/message')
app.register_blueprint(video, url_prefix='/videos')

bootstrap = Bootstrap(app)
socketio.init_app(app)
app.secret_key = 'asdkjfhsiw@#sf64461dasf#$%'


@app.route('/')
def index():
    username = current_user_name()
    template = render_template('index.html', username=username)
    r = set_salt_cookie(template)
    log('建立了访问', request.remote_addr, ':', request.cookies.get('cookie'))
    return r


@app.before_first_request
def set_cookie():
    print('first')
    url = redirect(request.url)
    r = set_salt_cookie(url)
    return r


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


if __name__ == '__main__':
    config = dict(
        host="0.0.0.0",
        port=5000,
        debug=True,
    )
    socketio.run(app, **config)
