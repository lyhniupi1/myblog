import os
import click
from flask import Flask
from flask_login import current_user
from myblog.settings import config
from myblog.models import Admin, Comment, Category, Post, Link
from myblog.blueprints.auth import auth_bp
from myblog.blueprints.blog import blog_bp
from myblog.blueprints.admin import admin_bp
from myblog.blueprints.ckeditor_upload import upload_bp
from myblog.extensions import bootstrap, db, login_manager, csrf, ckeditor, mail, moment, migrate, assets_env, css, js
from flask_assets import Environment, Bundle

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv("FLASK_CONFIG","development")
    app = Flask('myblog')
    app.config.from_object(config[config_name])

    register_emails(app)
    register_blueprints(app)
    register_extensions(app)
    register_template_context(app)
    register_shell_context(app)
    register_commands(app)
    register_assets(app)
    return app


def register_commands(app):
    @app.cli.command()
    @click.option("--category",default=10,help="category")
    @click.option("--post",default=50,help="post")
    @click.option("--comment",default=500,help="comment")
    def forge(category,post,comment):
        from myblog.fakes import fake_admin,fake_categories,fake_comments,fake_posts
        db.drop_all()
        db.create_all()

        click.echo("生成管理员")
        fake_admin()

        click.echo("生成分类")
        fake_categories()

        click.echo("生成博文")
        fake_posts(post)

        click.echo("生成评论")
        fake_comments(comment)

        click.echo("生成完成")

    @app.cli.command()
    @click.option("--drop", is_flag=True, help="数据库初始化")
    def initdb(drop):
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo("数据库已清空")
        db.create_all()
        click.echo("数据库初始化完成")

    @app.cli.command()
    @click.option('--username', prompt=True, help='The username used to login.')
    @click.option('--password', prompt=True, hide_input=True,
                  confirmation_prompt=True, help='The password used to login.')
    def init(username, password):
        """Building Bluelog, just for you."""

        click.echo('Initializing the database...')
        db.create_all()

        admin = Admin.query.first()
        if admin is not None:
            click.echo('The administrator already exists, updating...')
            admin.username = username
            admin.set_password(password)
        else:
            click.echo('Creating the temporary administrator account...')
            admin = Admin(
                username="ligewudi",
                blog_title='ligewudi',
                blog_sub_title="cookie!",
                name='lyh',
                about="a little bit of niubi",
            )
            admin.set_password(password)
            db.session.add(admin)

        category = Category.query.first()
        if category is None:
            click.echo('Creating the default category...')
            category = Category(name='Default')
            db.session.add(category)

        db.session.commit()
        click.echo('Done.')


def register_template_context(app):
    @app.context_processor
    def make_template_context():
        links = Link.query.all()
        admin = Admin.query.first()
        categories = Category.query.order_by(Category.name).all()
        if current_user.is_authenticated:
            unread_comments = Comment.query.filter_by(reviewed=False).count()
        else:
            unread_comments = None
        return(dict(admin=admin, categories=categories, links=links, unread_comments=unread_comments))


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, Admin=Admin, Post=Post, Category=Category, Comment=Comment)


def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    csrf.exempt(upload_bp)
    ckeditor.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    # toolbar.init_app(app)
    migrate.init_app(app, db)


def register_blueprints(app):
    app.register_blueprint(auth_bp,url_prefix="/auth")
    app.register_blueprint(blog_bp)
    app.register_blueprint(admin_bp,url_prefix="/admin")
    app.register_blueprint(upload_bp)


def register_emails(app):
    app.config.update(
        MAIL_SERVER='smtp.qq.com',
        MAIL_PORT=465,
        MAIL_USE_SSL=True,
        MAIL_USE_TLS=False,
        MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
        MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    )


def register_assets(app):
    assets_env.init_app(app)
    assets_env.register('main_js', js)
    assets_env.register('main_css', css)

    return app