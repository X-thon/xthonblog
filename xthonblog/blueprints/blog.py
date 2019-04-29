from flask import Blueprint, render_template, redirect, url_for, flash, request, abort, make_response, current_app
from flask_login import current_user

from xthonblog.extensions import db
from xthonblog.forms import CommentForm
from xthonblog.models import Post, Category, Admin



blog_bp = Blueprint("blog", __name__)



# 定义首页路由
@blog_bp.route("/")
def index():
    """
    describe：This page is the blog's home page. First visit the blog will direct to this page.
              This page will display the article record after paging and Navigation Bar.
    :return:
    """
    #将所有博文按照时间戳排序之后取出；传入模版；
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLUELOG_POST_PER_PAGE']
    #注意使用.objects方法别漏了()
    pagination = Post.objects().order_by("timestamp").paginate(page, per_page=per_page)
    posts = pagination.items
    return render_template("blog/index.html", pagination=pagination, posts=posts)


#定义选择分类后的页面
#mongodb中id为字符串型;自定义了一个int型的
@blog_bp.route("/category/<int:category_id>")
def show_category(category_id):
    #分类不存在则导向404
    category = Category.objects.get_or_404(id=category_id)
    page = request.args.get("page", 1, type=int)
    per_page = current_app.config['BLUELOG_POST_PER_PAGE']
    
    pagination = Post.objects(belong=category).order_by("timestamp").paginate(page, per_page=per_page)
    #获取该分类下的所有文章
    posts = pagination.items
    return render_template("blog/category.html", category=category, pagination=pagination, posts=posts)


#定义显示具体文章页面的路由
@blog_bp.route("/posts/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
    #查询并获取博文信息
    post = Post.objects.get_or_404(id=post_id)
    
    return render_template("blog/post.html", post=post)