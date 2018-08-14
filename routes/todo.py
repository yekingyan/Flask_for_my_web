from flask import (
    Blueprint,
    render_template,
    redirect,
    request,
    url_for,
)
from models.todo import Todo
from tools import log

# 创建蓝图,蓝图名为main
main = Blueprint('todo', __name__)


@main.route('/')
def index():
    todo_list = Todo.all()
    return render_template('todo.html', todos=todo_list)


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
