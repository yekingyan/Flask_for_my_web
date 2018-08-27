from flask import (
    Blueprint,
    render_template,
    redirect,
    request,
    url_for,
    make_response,
    flash,
)
from models.todo import Todo
from tools import log
from models.user import (
    salt,
    current_user_name,
)


# 创建蓝图,蓝图名为main
main = Blueprint('todo', __name__)


@main.route('/')
def index():
    todo_list = Todo.all_by_cookie()
    username = current_user_name()
    template = render_template('todo.html', todos=todo_list, title='Todo', username=username)
    r = make_response(template)
    if request.cookies.get('cookie') is None:
        r.set_cookie('cookie', salt(), max_age=2419200)
    return r


@main.route('/add', methods=['post'])
def add():
    form = request.form
    print(form)
    t = Todo.new_without_save(form)

    if t.title == ' ' or len(t.title) == 0:
        flash("人生在世总是要干点什么的")
    else:
        t.save()
    return redirect(url_for('todo.index'))


@main.route('/delete/<int:todo_id>')
def delete(todo_id):
    log("tying delete id---", todo_id)
    if Todo.id_for_cookie(todo_id) == request.cookies.get('cookie'):
        t = Todo.delete(todo_id)
        log("deleted id:", todo_id)
        # flash("删除成功")
    else:
        flash("你要删除火星上面的东西吗")
    return redirect(url_for('.index'))