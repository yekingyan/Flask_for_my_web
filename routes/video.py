from flask import (
    Blueprint,
    render_template,
)
from models.user import current_user_name

# 创建蓝图,蓝图名为main
main = Blueprint('video', __name__)


@main.route('/')
def index():
    username = current_user_name()
    return render_template('video.html', title='视频', username=username)