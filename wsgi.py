#!/usr/bin/env python3
import sys
from os.path import abspath
from os.path import dirname


# 设置当前目录为工作目录，避免在阿帕奇上出错
sys.path.insert(0, abspath(dirname(__file__)))

# 引入app.py
import app
# 规定的协议
# 必须要有一个叫做application的变量
# gunicorn 就要这个变量
# 变量值必须是Flask实例
application =app.app