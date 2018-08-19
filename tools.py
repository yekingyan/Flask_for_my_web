import time


def strftime(ttint):
    """转time.time()格式为人类可读"""
    format = '%Y%m%d-%H:%M:%S'
    value = time.localtime(int(ttint))
    dt = time.strftime(format, value)
    return dt


def log(*args, **kwargs):
    """
    写入log.txt文件，带有输出时间
    """
    format = '%Y%m%d-%H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    with open('log.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)





# if __name__ == '__main__':
#     format = '%Y%m%d-%H:%M:%S'
#     value = time.localtime(int(time.time()))
#     dt = time.strftime(format, value)
#     print(dt)