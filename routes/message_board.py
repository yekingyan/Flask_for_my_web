from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
)
from models.message_board import MessageBoard
from models.user import current_user_name

main = Blueprint('message', __name__)


@main.route('/')
def index():
    username = current_user_name()
    all_message = MessageBoard.all_message()
    cookie = request.cookies.get('cookie')
    guest = MessageBoard.find_by(cookie=cookie).message_user
    print((guest,))
    return render_template(
        'message_board.html',
        title="留言板",
        username=username,
        message=all_message,
        guest=guest,
        none=None,
    )


@main.route('/add', methods=['post'])
def add():
    form = request.form
    m = MessageBoard.new_without_save(form)
    # 第一次之后就不用输临时用户名，则m.message为空,此时要指定旧数据中的用户名给它
    if m.message_user is '':
        m.message_user = MessageBoard.find_by(cookie=request.cookies.get('cookie')).message_user
        m.save()
    # 用于第一次输入临时用户名找到是否存在cookie，有值就表名用户名重复了
    check_cookie = MessageBoard.find_by(message_user=m.message_user).cookie

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
    # 首页会自动设cookie
    elif check_cookie is '' or check_cookie is None:
        return redirect(url_for('index'))
    else:
        m.save()
    return redirect(url_for('.index'))


@main.route('/delete/<id>')
def delete(id):
    MessageBoard.delete(id)
    return redirect(url_for(".index"))