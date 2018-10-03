from flask import (
    Blueprint,
    render_template,
)


# 创建蓝图,蓝图名为main
main = Blueprint('video', __name__)


@main.route('/')
def index():
    return render_template('video.html')