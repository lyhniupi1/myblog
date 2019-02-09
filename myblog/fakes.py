from myblog.models import Admin, Category, Post, Comment, Link
from myblog.extensions import db
from faker import Faker
import random

fake = Faker()

def fake_admin():
    admin = Admin(
        username = "ligewudi",
        blog_title='ligewudi',
        blog_sub_title="cookie!",
        name='lyh',
        about="a little bit of niubi",
    )
    admin.set_password("123321123")
    db.session.add(admin)
    db.session.commit()

def fake_categories():
    category = Category(name="默认分类")
    db.session.add(category)
    category1 = Category(name="Flask")
    category2 = Category(name="Leetcode")
    category3 = Category(name="Python")
    category4 = Category(name="Basketball")
    db.session.add(category1)
    db.session.add(category2)
    db.session.add(category3)
    db.session.add(category4)
    db.session.commit()

def fake_posts(count=50):
    for i in range(count):
        post = Post(
            title = fake.sentence(),
            body=fake.text(2000),
            category=Category.query.get(random.randint(1,Category.query.count()))
        )
        db.session.add(post)
    db.session.commit()

def fake_comments(count=500):
    for  i in range(count):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=True,
            post=Post.query.get(random.randint(1,Post.query.count()))
        )
        db.session.add(comment)

    salt = int(count * 0.1)
    for i  in range(salt):
        #未读评论
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=False,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)

        #作者评论
        comment = Comment(
            author='Lige',
            email='k1003@qq.com',
            site='ligewudi.com',
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            from_admin=True,
            reviewed=True,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)
    db.session.commit()

    #replies
    for i in range(salt):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=True,
            replied = Comment.query.get(random.randint(1, Comment.query.count())),
            post = Post.query.get(random.randint(1,Post.query.count()))
    )
        db.session.add(comment)
    db.session.commit()

def fake_links():
    twitter = Link(name='Twitter', url='#')
    facebook = Link(name='Facebook', url='#')
    linkedin = Link(name='LinkedIn', url='#')
    google = Link(name='Google+', url='#')
    db.session.add_all([twitter, facebook, linkedin, google])
    db.session.commit()