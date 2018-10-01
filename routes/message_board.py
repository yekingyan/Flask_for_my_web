from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
)
from models.message_board import (
    MessageBoard,
    guest,
)
from models.user import (
    current_user_name,
    set_salt_cookie,
)
from tools import log
from flask_socketio import SocketIO, emit


socketio = SocketIO()
main = Blueprint('message', __name__)


@main.route('/')
def index():
    username = current_user_name()
    all_message = MessageBoard.all_message()
    cookie = request.cookies.get('cookie')
    guest = MessageBoard.find_by(cookie=cookie).message_user
    template = render_template(
        'message_board.html',
        title="留言板",
        username=username,
        message=all_message,
        guest=guest,
        none=None,
    )
    r = set_salt_cookie(template)
    return r


@main.route('/add', methods=['post'])
def add():
    form = request.form
    # print(form, "testttt")
    m, check_cookie = guest(form)
    all_user = MessageBoard.all_user()
    # 判断内容是否空白
    if m.content == ' ' or len(m.content) == 0:
        flash("你说得很空白无力")
    # 排除重名
    elif m.message_user is '' and m.user is None:
        flash("给自己一个好听的昵称吧")
    # 查看cookie是否匹配
    elif (check_cookie is not '' or check_cookie is not None) \
            and check_cookie != request.cookies.get('cookie') \
            and m.message_user in all_user \
            and m.user is None:
        flash("好名字都被别人取了，再想一个昵称吧")
    else:
        m.save()
        log('save', form)
    return redirect(url_for('.index'))


@main.route('/delete/<id>')
def delete(id):
    MessageBoard.delete(id)
    return redirect(url_for(".index"))


# 连接之后返回所有聊天信息
@socketio.on('connect_event', namespace='/chat')
def connected_msg(msg):
    log("来自客户端的：", msg)
    all_message = MessageBoard.all_message()
    dict_ = {}
    [dict_.update({n: m.__dict__}) for n, m in enumerate(all_message)]
    for d in dict_.values():
        del d['cookie'], d["_id"], d['delete']
    # print(len(all_message))
    # print(json.dumps(dict_))
    emit('server_response', {'data': dict_})


# 聊天信息的接收与响应
@socketio.on('client_event', namespace='/chat')
def connected_msg(form):
    log("来自客户端的：", form)
    m, check_cookie = guest(form)
    all_user = MessageBoard.all_user()
    # 判断内容是否空白
    if m.content == ' ' or len(m.content) == 0:
        emit('flash_message', {'flash': "你说得很空白无力"})
    # 排除重名
    elif m.message_user is '' and m.user is None:
        emit('flash_message', {'flash': "给自己一个好听的昵称吧"})
    # 查看cookie是否匹配
    elif (check_cookie is not '' or check_cookie is not None) \
            and check_cookie != request.cookies.get('cookie') \
            and m.message_user in all_user \
            and m.user is None:
        emit('flash_message', {'flash': "好名字都被别人取了，再想一个昵称吧"})
    else:
        m.save()
        print('save')
    # return redirect(url_for('.index'))
        emit('new_message', {
            'user': m.user,
            'message_user': m.message_user,
            'id': m.id,
            'ct': m.ct,
            'content': m.content,
        },
             broadcast=True,
             )


# 删除
@socketio.on('delete_msg', namespace='/chat')
def delete_msg(msg):
    log("尝试删除", msg)
    m_id = msg['id']
    m = MessageBoard.delete(m_id)
    if type(m) == dict:
        emit('flash_message', m)
    else:
        emit('remove', {'id': m.id}, broadcast=True)