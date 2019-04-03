#!/usr/bin/env bash
# 设置项目开机自启
#chkconfig: 2345 80 90

source /root/venvs/ljx/bin/activate

cd /root/apps/ljx/confs

uwsgi --ini uwsgi7777.ini
uwsgi --ini uwsgi7778.ini
uwsgi --ini uwsgi7779.ini
uwsgi --ini uwsgi7780.ini

exit 0
