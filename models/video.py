import os
from tools import strftime


def video_names(*agrs):
    """
    主要用于poster文件，poster与video名字相同
    :param agrs: 路径名
    :return: 路径 和 视频名字对应创建时间的列表（元素为字典）
    """
    # poster的路径
    dir_poster = os.path.join(*agrs)
    # 文件名
    names = os.listdir(dir_poster)
    # # 去掉'.jpg后缀'.生成文件名与创建时间对应的字典
    name_and_time = [
        {name[:-4]: os.path.getctime(os.path.join(dir_poster, name))}
        for name in names
    ]

    # 去掉'poster',更替windows下的'\'
    path = dir_poster[:-6]
    # 按时间排序,降序
    name_and_time.sort(key=lambda x: list(x.values())[0], reverse=True)
    # 格式化时间
    name_time = [{k: strftime(v)[:-3]} for video in name_and_time for k, v in video.items()]
    return path, name_time


cyanide_path, cyanide_videos = video_names('static', 'videos', 'Cyanide_and_Happiness', 'poster')



