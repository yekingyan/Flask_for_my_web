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



"""
web.conf 配置文件 以.conf结尾
[program:web]
command=/usr/bin/gunicorn wsgi --bind 0.0.0.0:80 --pid /tmp/web.pid
directory=/home/xiao_web13/yhj
autostart=true
autorestart=true

建立一个软连接
ln -s /home/web/yhj/conf/web.conf /etc/supervisor/conf.d/web.conf


web.nginx 配置文件 监听80，反向到5000
server {
    listen 80;
    location / {
        proxy_pass http://localhost:5000;
    }
}

建立一个软连接 nginx不强制以.nginx结尾
ln -s /home/web/yhj/conf/web.nginx /etc/nginx/sites-enabled/web
"""