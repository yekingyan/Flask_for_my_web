import string
import random
from flask import request


def salt():
    """返回16位随机字符串"""
    str_ascii = string.ascii_letters
    # print(str_ascii)
    str_digits = string.digits
    # print(str_digits)
    salt16 = ''.join(random.sample(str_ascii + str_digits, 16))
    return salt16


def get_cookie():
    c = request.cookies.get('cookie')
    return c


if __name__ == '__main__':
    print(salt())
