from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
)
from models.message_board import MessageBoard
from models.user import current_user_name

main = Blueprint('message', __name__)


@main.route('/')
def index():
    username = current_user_name()
    all_message = MessageBoard.all_message()
    return render_template('message_board.html', title="留言板", username=username, message=all_message)


@main.route('/add', methods=['post'])
def add():
    form = request.form
    print(form)
    m = MessageBoard.new_without_save(form)
    all_user = MessageBoard.all_user()
    # 判断内容是否空白
    if m.content == ' ' or len(m.content) == 0:
        flash("你说得很空白无力")
    # 排除重名
    elif m.message_user is None and m.user is None:
        flash("给自己一个名字吧")
    elif m.message_user in all_user and m.user is None:
        flash("好名字都被别人取了，再想一个昵称吧")
    else:
        m.save()
    return redirect(url_for('.index'))


@main.route('/delete/<id>')
def delete(id):
    MessageBoard.delete(id)
    return redirect(url_for(".index"))