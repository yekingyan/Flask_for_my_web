from flask import (
    Flask,
    request,
    render_template,
    make_response,
    redirect,
)
from flask_bootstrap import Bootstrap
from models.user import (
    salt,
    current_user_name,
    set_salt_cookie,
)
from routes.user import main as user
# 同级目录routes文件夹下todo.py
from routes.todo import main as todo
from routes.video import main as video
from routes.message_board import main as message, socketio


# 实例化Flask
app = Flask(__name__)

# 注册蓝图，url_prefix为每个main蓝图路由加上前缀
app.register_blueprint(todo, url_prefix='/todo')
app.register_blueprint(user)
app.register_blueprint(message, url_prefix='/message')
app.register_blueprint(video, url_prefix='/video')

bootstrap = Bootstrap(app)
socketio.init_app(app)
app.secret_key = 'asdkjfhsiw@#sf64461dasf#$%'


@app.route('/')
def index():
    username = current_user_name()
    template = render_template('index.html', username=username)
    r = set_salt_cookie(template)
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


# # 纪录连接状态
# @socketio.on('connect_event')
# def connected_msg(msg):
#     print("来自客户端的：", msg)
#     emit('server_response', {'data': msg['data']})
#
#
# # 聊天信息的接收与响应
# @socketio.on('client_event')
# def connected_msg(msg):
#     print("发给客户端的：", msg)
#     emit('new_message', {'data': msg['data']})


if __name__ == '__main__':
    config = dict(
        host="0.0.0.0",
        port=5000,
        debug=True,
    )
    socketio.run(app, **config)
