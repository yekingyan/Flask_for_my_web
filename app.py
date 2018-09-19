from flask import (
    Flask,
    request,
    render_template,
    make_response,
)
from flask_bootstrap import Bootstrap
from models.user import (
    salt,
    current_user_name,
)
from routes.user import main as user
# 同级目录routes文件夹下todo.py
from routes.todo import main as todo
from routes.message_board import main as message
from flask_socketio import SocketIO, emit

# 实例化Flask
app = Flask(__name__)

# 注册蓝图，url_prefix为每个main蓝图路由加上前缀
app.register_blueprint(todo, url_prefix='/todo')
app.register_blueprint(user)
app.register_blueprint(message, url_prefix='/message')

bootstrap = Bootstrap(app)
socketio = SocketIO()
socketio.init_app(app)
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


@socketio.on('connect_event')
def connected_msg(msg):
    print("来自客户端的：", msg)
    emit('server_response', {'data': msg['data']})


if __name__ == '__main__':
    config = dict(
        host="0.0.0.0",
        port=5000,
        debug=True,
    )
    socketio.run(app, **config)
