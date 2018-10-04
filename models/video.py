import os


def video_names(*agrs):
    """
    主要用于poster文件，poster与video名字相同
    :param agrs: 路径名
    :return: 路径 和 视频名字的列表
    """
    dir_poster = os.path.join(*agrs)
    names = os.listdir(dir_poster)
    # 去掉'.jpg后缀'
    names_format = [i[:-4] for i in names]
    # 去掉'poster',更替windows下的'\'
    path = dir_poster[:-6]
    return path, names_format


cyanide_path, cyanide_videos = video_names('static', 'videos', 'Cyanide_and_Happiness', 'poster')


