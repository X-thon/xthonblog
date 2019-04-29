from datetime import datetime

from flask_login import UserMixin
from xthonblog.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash




# 定义管理员用户类
class Admin(db.Document, UserMixin):
    meta = {
        'collection': 'admin',
        'ordering': ['-create_at']
    }

    username = db.StringField(max_length=20)
    create_at = db.DateTimeField(default=datetime.now)
    # 密码存储哈希加密之后的值
    password_hash = db.StringField(max_length=128)
    # 博客的正副标题
    blog_title = db.StringField(max_length=60)
    blog_sub_title = db.StringField(max_length=100)
    # 要显示的博客主人名
    name = db.StringField(max_length=30)
    location = db.StringField(max_length=20)
    introduction = db.StringField(max_length=80)

    # 密码加密函数
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # 密码验证函数
    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Category(db.Document):
    meta = {
        'collection': 'category',
        'ordering': ['-create_at']
    }
    id = db.IntField(primary_key=True)
    name = db.StringField()
    posts = db.ListField(db.ReferenceField("Post"))


class Post(db.Document):
    meta = {
        'collection': 'post',
        'ordering': ['-create_at']
    }
    id = db.IntField(primary_key=True)
    title = db.StringField()
    body = db.StringField()
    timestamp = db.DateTimeField(default=datetime.utcnow)
    # 属于那个分类
    belong = db.ReferenceField(Category)


class Link(db.Document):
    meta = {
        'collection': 'link',
        'ordering': ['-create_at']
    }
    name = db.StringField()
    url = db.StringField()