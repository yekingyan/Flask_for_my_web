from flask import (
    Blueprint,
    render_template,
    redirect,
    request,
    url_for,
    make_response,
)
from models.todo import Todo
from tools import log
from models.user import (
    get_cookie,
    salt,
)


# 创建蓝图,蓝图名为main
main = Blueprint('todo', __name__)


@main.route('/')
def index():
    todo_list = Todo.all()
    template = render_template('todo.html', todos=todo_list)
    r = make_response(template)
    if get_cookie() is None:
        r.set_cookie('cookie', salt())
    return r


@main.route('/add', methods=['post'])
def add():
    form = request.form
    t = Todo.new(form)
    t.save()
    return redirect(url_for('todo.index'))


@main.route('/delete/<int:todo_id>')
def delete(todo_id):
    log("debug,todoid---", todo_id)
    t = Todo.delete(todo_id)
    return redirect(url_for('.index'))
