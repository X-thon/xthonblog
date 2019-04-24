#存储虚拟数据生成函数
from random import randint
from faker import Faker
from sqlalchemy.exc import IntegrityError

from xthonblog.models import Admin, Category, Post, Comment, Link
from xthonblog import db

fake = Faker()

def fake_admin():
    admin = Admin(
        username='admin',
        blog_title='xthonblog',
        blog_sub_title='None, this not reality.',
        name='Xthon',
        #about='Aha, I, Xthon, had a fun time as a member of CHAM...',
        location='China, Nanjing',
        introduction="Welcome to my blog! I will write my thinks in here. I love this."
    )
    #调用
    admin.set_password('qweasdzxc123')
    db.session.add(admin)
    db.session.commit()



def fake_categories(count=10):
    category = Category(name='Default')
    db.session.add(category)

    for i in range(count):
        #使用fake.word()生成虚拟词
        category = Category(name=fake.word())
        db.session.add(category)
        try:
            db.session.commit()
        #重名错误
        except IntegrityError:
            db.session.rollback()



def fake_posts(count=30):
    for i in range(count):
        post = Post(
            title=fake.sentence(),
            body=fake.text(2000),
            #在Category类中随机获取一个
            category=Category.query.get(randint(1, Category.query.count())),
            timestamp=fake.date_time_this_year()
        )

        db.session.add(post)
    db.session.commit()



def fake_comments(count=500):
    for i in range(count):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=True,
            post=Post.query.get(randint(1, Post.query.count()))
        )
        db.session.add(comment)

    #添加未被审阅的评论
    salt = int(count * 0.1)
    for i in range(salt):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=False,
            post=Post.query.get(randint(1, Post.query.count()))
        )
        db.session.add(comment)

        #添加来自管理员的评论
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            from_admin=True,
            reviewed=False,
            post=Post.query.get(randint(1, Post.query.count()))
        )
        db.session.add(comment)
    db.session.commit()

    #添加回复
    for i in range(salt):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=False,
            replied=Comment.query.get(randint(1, Comment.query.count())),
            post=Post.query.get(randint(1, Post.query.count()))
        )
        db.session.add(comment)
    db.session.commit()



def fake_link():
    github = Link(name="github", url="#")
    twitter = Link(name="twitter", url="#")
    weibo = Link(name="weibo", url="#")
    steam = Link(name="steam", url="#")
    db.session.add_all([github, twitter, weibo, steam])
    db.session.commit()