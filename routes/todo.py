from flask import (
    Blueprint,
    render_template,
    redirect,
    request,
    url_for,
    make_response,
    flash,
    jsonify,
)
from models.todo import Todo
from tools import (
    log,
    strftime,
)
from models.user import (
    salt,
    current_user_name,
)


# 创建蓝图,蓝图名为main
main = Blueprint('todo', __name__)


@main.route('/')
def index():
    # 游客数据用cookie。
    if current_user_name() is None:
        todo_list = Todo.all_by_cookie()
    # 用户数据优于session，用户优先
    else:
        todo_list = Todo.all_by_user()

    username = current_user_name()
    template = render_template('todo.html', todos=todo_list, title='Todo', username=username)
    r = make_response(template)
    if request.cookies.get('cookie') is None:
        r.set_cookie('cookie', salt(), max_age=2419200)
    return r


@main.route('/add', methods=['post'])
def add():
    if request.method == 'POST' or request.method == 'post':
        form = request.json
        if form is None:
            form = request.form
    print(form)
    t = Todo.new_without_save(form)

    if t.title == ' ' or len(t.title) == 0:
        flash("人生在世总是要干点什么的")
    else:
        t.save()
    # return redirect(url_for('todo.index'))
    return jsonify({
        "id": t.id,
        "ct": strftime(t.ct),
        "title": t.title,
    })


@main.route('/delete/<int:todo_id>')
def delete(todo_id):
    log("tying delete id---", todo_id)
    u_name = current_user_name()
    t = Todo.find_by(id=todo_id)
    # 用户身份删除
    if u_name is not None and t.user == u_name:
        Todo.delete(todo_id)
    # 游客身份删除
    elif t is not None and t.cookie == request.cookies.get('cookie'):
        # 游客不能删除已注册给用户的数据
        if t.user is None:
            Todo.delete(todo_id)
            log("deleted id:", todo_id)
        else:
            flash("离线状态不能删除在登陆状态时所添加的数据")
    else:
        flash("你要删除火星上面的东西吗")
    return redirect(url_for('.index'))