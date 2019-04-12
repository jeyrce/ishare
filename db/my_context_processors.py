# coding: utf-8
"""
Created by Jeeysie.Ru at 19-3-27 下午2:26, for any more contact me with jeeysie@gmail.com.
Here is the descriptions and some popurse of the file:
    0. 自定义全局上下文
"""
from ljx import settings
from db.utils import ContextUtil as ctx


def site(request):
    # 关于站点的静态信息
    return {'SITE': settings.SITE}


def cats(request):
    # 站点分类文件
    return {
        'A_CATS': ctx.cats('A'),
        'a_cat': '文学创作',
        'B_CATS': ctx.cats('B'),
        'b_cat': '技术干货',
    }


def site_count(request):
    # 关于站点的统计信息
    return {'SITE_CNT': {
        'run': ctx.run_days(),  # 运行天数
        'origin': ctx.origin_art_cnt(),  # 原创文章数
        'copy': ctx.copy_art_cnt(),  # 转载文章,
        'visit': ctx.visit_cnt(),  # 总访问数
        'today_visit': ctx.today_visit_cnt(),  # 今日访问
    }}


def most_read(request):
    # 点击排行
    return {'MOST_READ': ctx.most_read()}


def notice(request):
    # 网站公告
    return {'NOTICE': ctx.notice()}


def recommend(request):
    # 推荐阅读
    return {'RECOMMEND': ctx.recommend()}
