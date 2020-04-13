from flask import Blueprint, render_template, redirect, url_for, flash, request, abort, make_response, current_app
from flask_login import current_user

import requests
from pprint import pprint
from datetime import datetime

from xthonblog.extensions import db, cache
from xthonblog.forms import CommentForm
from xthonblog.models import Post, Category, Comment, Admin



blog_bp = Blueprint("blog", __name__)



#定义首页路由
@blog_bp.route("/")
@cache.cached(timeout=60)
def index():
    """
    describe：This page is the blog's home page. First visit the blog will direct to this page.
              This page will display the article record after paging and Navigation Bar.
    :return:
    """
    #将所有博文按照时间戳排序之后取出；传入模版；
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLUELOG_POST_PER_PAGE']
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=per_page)
    posts = pagination.items
    return render_template("blog/index.html", pagination=pagination, posts=posts)


# #定义博客相关页面的路由
# @blog_bp.route("/about")
# def about():
#     """

#     :return:
#     """
#     return None



#定义显示具体文章页面的路由
@blog_bp.route("/posts/<int:post_id>", methods=["GET", "POST"])
@cache.cached(timeout=60)
def show_post(post_id):
    #查询并获取博文信息
    post = Post.query.get_or_404(post_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLUELOG_COMMENT_PER_PAGE']
    pagination = Comment.query.with_parent(post).filter_by(reviewed=True).order_by(Comment.timestamp.asc()).paginate(
        page, per_page)
    comments = pagination.items

    #如果用户状态为已登陆
    #否则
    form = CommentForm()

    #如果在当页提交了评论表单
    return render_template("blog/post.html", post=post, pagination=pagination, form=form, comments=comments)



#定义选择分类后的页面
@blog_bp.route("/category/<int:category_id>")
def show_category(category_id):
    #分类不存在则导向404
    category = Category.query.get_or_404(category_id)
    page = request.args.get("page", 1, type=int)
    per_page = current_app.config['BLUELOG_POST_PER_PAGE']
    pagination = Post.query.with_parent(category).order_by(Post.timestamp.desc()).paginate(page, per_page)
    #获取该分类下的所有文章
    posts = pagination.items
    return render_template("blog/category.html", category=category, pagination=pagination, posts=posts)



# #定义回复评论的路由接口
# @blog_bp.route("/reply/comment/<int:comment_id>")
# def reply_comment(comment_id):
#     return None



# 定义显示天气的页面
@blog_bp.route("/weather")
def show_weather():
    #通过api请求天气数据,并使用解析器将其json数据转换为python字典对象
    r = requests.get("https://route.showapi.com/9-2?area=南京&need3HourForcast=1&needAlarm=0&needHourData=1&needIndex=1&needMoreDay=1&showapi_appid=130858&showapi_sign=56a76dc831144c5aa6b6ad1bcb6b3e14").json()

    # 转换字符串常量日期为标准格式的小函数
    def trans_date(date: str) -> str:
        d = datetime.strptime(date, '%Y%m%d')
        res = datetime.strftime(d, '%m月%d日')
        return res

    days = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    # 生成长度为5的数组，每个元素为一个字典对象，存放该天天气的属性
    five_day_weather_data = [ dict() for i in range(5) ]

    weather_data = r["showapi_res_body"]
    city_name = r["showapi_res_body"]["cityInfo"]["c5"]

    for i in range(5):
        target_key = "f" + str(i+1)
        cur_day = five_day_weather_data[i]
        cur_day["city_name"] = city_name
        cur_day["day"] = trans_date(str(weather_data[target_key]["day"]))
        cur_day["day_air_temperature"] = weather_data[target_key]["day_air_temperature"]
        cur_day["night_air_temperature"] = weather_data[target_key]["night_air_temperature"]
        cur_day["weekday"] = days[int(weather_data[target_key]["weekday"])-1]
        cur_day["day_wind_direction"] = weather_data[target_key]["day_wind_direction"]
        cur_day["night_wind_direction"] = weather_data[target_key]["night_wind_direction"]
        cur_day["day_weather"] = weather_data[target_key]["day_weather"]
        cur_day["night_weather"] = weather_data[target_key]["night_weather"]
        cur_day["day_wind_power"] = weather_data[target_key]["day_wind_power"]
        cur_day["night_wind_power"] = weather_data[target_key]["night_wind_power"]
        cur_day["aqi"] = weather_data[target_key]["index"]["aqi"]["title"]
        cur_day["ziwaixian_power"] = weather_data[target_key]["ziwaixian"]
        cur_day["clothes_tip"] = weather_data[target_key]["index"]["clothes"]["desc"]

    # 构造今日天气趋势的数据
    target_data = r["showapi_res_body"]["f1"]["3hourForcast"]
    current_day_tend_data = [ dict() for _ in range(12) ]
    #由于数据格式不够规范，故只好一个一个取值
    #0时气温
    current_day_tend_data[0]["time"] = "00:00"
    current_day_tend_data[0]["temperature"] = target_data[-3]["temperature"]
    current_day_tend_data[0]["weather"] = target_data[-3]["weather"]
    #2时气温
    current_day_tend_data[1]["time"] = "02:00"
    current_day_tend_data[1]["temperature"] = target_data[-3]["temperature"]
    current_day_tend_data[1]["weather"] = target_data[-3]["weather"]
    #4时气温
    current_day_tend_data[2]["time"] = "04:00"
    current_day_tend_data[2]["temperature"] = target_data[-2]["temperature"]
    current_day_tend_data[2]["weather"] = target_data[-2]["weather"]
    #6时气温
    current_day_tend_data[3]["time"] = "06:00"
    current_day_tend_data[3]["temperature"] = target_data[-2]["temperature"]
    current_day_tend_data[3]["weather"] = target_data[-2]["weather"]
    #8时气温
    current_day_tend_data[4]["time"] = "08:00"
    current_day_tend_data[4]["temperature"] = target_data[0]["temperature"]
    current_day_tend_data[4]["weather"] = target_data[0]["weather"]
    #10时气温
    current_day_tend_data[5]["time"] = "10:00"
    current_day_tend_data[5]["temperature"] = target_data[0]["temperature"]
    current_day_tend_data[5]["weather"] = target_data[0]["weather"]
    #12时气温
    current_day_tend_data[6]["time"] = "12:00"
    current_day_tend_data[6]["temperature"] = target_data[1]["temperature"]
    current_day_tend_data[6]["weather"] = target_data[1]["weather"]
    #14时气温
    current_day_tend_data[7]["time"] = "14:00"
    current_day_tend_data[7]["temperature"] = target_data[1]["temperature"]
    current_day_tend_data[7]["weather"] = target_data[1]["weather"]
    #16时气温
    current_day_tend_data[8]["time"] = "16:00"
    current_day_tend_data[8]["temperature"] = target_data[2]["temperature"]
    current_day_tend_data[8]["weather"] = target_data[2]["weather"]
    #18时气温
    current_day_tend_data[9]["time"] = "18:00"
    current_day_tend_data[9]["temperature"] = target_data[3]["temperature"]
    current_day_tend_data[9]["weather"] = target_data[3]["weather"]
    #20时气温
    current_day_tend_data[10]["time"] = "20:00"
    current_day_tend_data[10]["temperature"] = target_data[3]["temperature"]
    current_day_tend_data[10]["weather"] = target_data[3]["weather"]
    #22时气温
    current_day_tend_data[11]["time"] = "22:00"
    current_day_tend_data[11]["temperature"] = target_data[4]["temperature"]
    current_day_tend_data[11]["weather"] = target_data[4]["weather"]

    cur_day_data = five_day_weather_data[0]
    return render_template("blog/weather.html", cur_day_data=cur_day_data, five_day_weather_data=five_day_weather_data, current_day_tend_data=current_day_tend_data)