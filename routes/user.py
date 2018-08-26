from flask import (
    Blueprint,
    render_template,
    redirect,
    request,
    url_for,
    make_response,
    flash,
    session,
)
from tools import log
from models.user import User

# 创建蓝图,蓝图名为main
main = Blueprint('user', __name__)


@main.route('/login')
def login():
    return render_template('login.html')


@main.route('/login/in', methods=['post'])
def sign_in():
    form = request.form
    log('login form', form)
    u = User.verify_user(form)
    log('u', u)
    if u is not None:
        # 设置session
        session['user_id'] = u.id
        # session永不过期
        session.permanent = True
        flash("登陆成功")
        return redirect(url_for('index'))
    else:
        flash("用户名或密码错误")
        return redirect(url_for('user.login'))


@main.route('/register')
def register():
    return render_template('register.html')


@main.route('/register/add', methods=['post'])
def add_user():
    form = request.form
    # log(form)
    u = User.add_new_user(form)
    # log(u)
    if "重名" in str(u):
        flash("该用户名已经被注册")
    if "用户名或密码太短了" in str(u):
        # todo 上线后把密码长度改为6位以上
        flash("请确保昵称长度2位以上，以及密码长度2位以上")
    else:
        flash("注册成功")
    return redirect(url_for('user.register'))


if __name__ == '__main__':
    print(type('是'))