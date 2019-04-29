#存储虚拟数据生成函数
from random import randint
from faker import Faker
from sqlalchemy.exc import IntegrityError

from xthonblog.models import Admin, Category, Post, Link
from xthonblog import db

fake = Faker()

category_name = []

def fake_admin():
    admin = Admin(
        username = 'admin',
        blog_title = "黄靖文的小博客",
        blog_sub_title = "Just write something in here.",
        name = "B16041211 黄靖文",
        location = "China, Nanjing",
        introduction = "Welcome to my blog! I will write my thinks in here."
    )
    admin.set_password("qweasdzxc")
    admin.save()


# count为要生成的分类数量
def fake_categories(count=5):
    category = Category(id=0, name="Default")
    category.save()
    category_name.append(category)
    for i in range(count):
        category = Category(id=i+1, name=fake.word())
        category.save()
        category_name.append(category)


def fake_posts(count=50):
    
    #categories = Category.objects
    for i in range(count):
        category = category_name[randint(0,5)]
        post = Post(
            id = i,
            title = fake.sentence(),
            body = fake.text(2000),
            timestamp = fake.date_time_this_year(),
            belong = category
        )
        category.posts.append(post)
        post.save()
        #You can only reference documents once they have been saved to the database: ['posts']
        category.save()
        
def fake_link():
    github = Link(name="github", url="#")
    twitter = Link(name="twitter", url="#")
    weibo = Link(name="weibo", url="#")
    steam = Link(name="steam", url="#")
    github.save()
    twitter.save()
    weibo.save()
    steam.save()