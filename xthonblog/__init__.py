import os

import click

from flask import Flask, render_template, request
from flask_login import current_user
from flask_sqlalchemy import get_debug_queries
from flask_wtf.csrf import CSRFError

#加载配置
from xthonblog.config import config
#加载蓝本
from xthonblog.blueprints.admin import admin_bp
from xthonblog.blueprints.auth import auth_bp
from xthonblog.blueprints.blog import blog_bp
#从扩展模块中加载扩展对象
from xthonblog.extensions import bootstrap, db, mail, moment, csrf, login_manager
#从数据库模型中加载模型对象
from xthonblog.models import Admin, Category, Post, Comment, Link
#加载配置
from xthonblog.config import config



#使用工程函数创建程序实例
def create_app(config_name=None):
    #如果未指定配置方案，则加载开发环境下的配置方案
    if config_name is None:
        config_name = os.getenv("FLASK_CONFIG", "development")
    
    #使用项目名初始化程序实例
    app = Flask("xthonblog")
    app.config.from_object(config[config_name])
    
    app.config['MONGODB_SETTINGS'] = {
        'db': 'smallblog',
        'host': 'localhost',
        'port': 27017
    }
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = "development key"
    
    #注册蓝本
    register_blueprints(app)
    register_extensions(app)
    register_template_context(app)
    #激活命令行
    register_commands(app)
    register_errors(app)
    #要注意一定要return app，否则flask运行后会找不到程序实例
    return app



#将蓝本注册到程序实例上，并为某些蓝本添加url前缀
def register_blueprints(app):
    app.register_blueprint(blog_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(auth_bp, url_prefix="/auth")



#初始化扩展对象
def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    moment.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)


#注册命令行上下文
def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, Admin=Admin, Post=Post, Category=Category)



#注册模版上下文
def register_template_context(app):
    @app.context_processor
    def make_template_context():
        admin = Admin.objects(username="admin").first()
        #根据名字排序，获取所有分类的记录
        categories = Category.objects.order_by("name").all()
        #获取文章的数量
        post_count = Post.objects.count()
        #获取链接
        links = Link.objects.all()
        return dict(admin=admin, categories=categories, post_count=post_count, links=links)




def register_errors(app):
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404




#注册命令行命令
def register_commands(app):


    @app.cli.command()
    @click.option('--category', default=10, help='Quantity of categories, default is 10.')
    @click.option('--post', default=50, help='Quantity of posts, default is 50.')
    @click.option('--comment', default=500, help='Quantity of comments, default is 500.')
    def forge(category, post, comment):
        """Generate fake data."""
        from xthonblog.fakers import fake_admin, fake_categories, fake_posts,  fake_link

        click.echo('Generating the administrator...')
        fake_admin()
        click.echo('Administrator generate done.')

        click.echo('Generating %d categories...' % category)
        fake_categories(category)
        click.echo('Categories generate done.')

        click.echo("Generating %d posts..." % post)
        fake_posts(post)
        click.echo('Posts generate done.')

        click.echo("Generating links...")
        fake_link()
        click.echo("Links generate done.")

        click.echo("Done.")