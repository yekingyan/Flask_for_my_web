import os
from tools import strftime
import re


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


def rename_file(path, match, format_):
    """
    重命名文件，如 "Stuck - Cyanide - YouTube.MP4" --> "Stuck.Mp4"
    rename_file(cyanide_path, ' - Cyanide', '.MP4')
    :param path: 文件夹路径名
    :param match: 要匹配的正则表达式（将删除所匹配及索引之后的所有字符）
    :param format_: 文件格式
    :return: None
    """

    all_names = os.listdir(path)
    new_names = []
    old_names = []
    # 编译的正则表达式
    del_postfix = re.compile(match)
    # 找到需要修改的名字
    for old_name in all_names:
        if match in old_name:
            index = del_postfix.search(old_name)
            # name + .Mp4
            print(index)
            name = re.sub(' ', '_', old_name[:index.start()])
            new_name = path + name + format_
            new_names.append(new_name)
            old_names.append(path + old_name)
    # print(old_names)
    # print(new_names)
    # # 重命名
    for i in range(len(new_names)):
        os.rename(old_names[i], new_names[i])


def check_lost(path):
    """
    查看视频名与略缩图名不一致的情况
    :param path:视频所有路径
    :return:
    """
    video_name = set(i[:-4] for i in os.listdir(path))
    poster_name = set(i[:-4] for i in os.listdir(os.path.join(path, 'poster')))
    print(poster_name ^ video_name)
    return poster_name ^ video_name


cyanide_path, cyanide_videos = video_names('static', 'videos', 'Cyanide_and_Happiness', 'poster')
others_path, others_videos = video_names('static', 'videos', 'Others', 'poster')

# rename_file(cyanide_path, ' - Cyanide', '.MP4')