from flask import (
    Blueprint,
    render_template,
    abort,
)
from models.user import current_user_name
from models.video import cyanide_path, cyanide_videos


# 创建蓝图,蓝图名为main
main = Blueprint('videos', __name__)


@main.route('/')
def index():
    return render_template('video_index.html',
                           title='视频',
                           username=current_user_name(),
                           cyanide=cyanide_videos,
                           cyanide_path=cyanide_path,
                           )


@main.route('cyanide/<name>')
def cyanide(name):
    if name not in cyanide_videos:
        abort(404)
    return render_template("video.html",
                           title=name,
                           username=current_user_name(),
                           path=cyanide_path
                           )