# coding: utf-8
"""
Created by Jeeyshe.Ru at 2019/4/10 下午8:08, for any more contact me with jeeyshe@gmail.com.
Here is the descriptions and some purpose of the file:
    0. celery异步任务和定时任务
"""

from ljx import celery_app


@celery_app.task()
def printx(self):
    f = open('task.txt', 'at', encoding='utf-8')
    for i in range(99):
        f.write(str(i).center(20, '+'))
        print(i)
    f.close()
