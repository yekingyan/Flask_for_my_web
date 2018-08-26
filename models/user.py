import string
import random
from flask import request


def salt():
    """
    返回16位随机字符串
    """
    # 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    str_ascii = string.ascii_letters
    # '0123456789'
    str_digits = string.digits
    # '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    str_punctuation = string.punctuation

    mix_str = str_ascii + str_digits + str_punctuation

    salt16 = ''.join(random.sample(mix_str, 16))
    return salt16


def get_cookie():
    c = request.cookies.get('cookie')
    return c


if __name__ == '__main__':
    print(salt())
