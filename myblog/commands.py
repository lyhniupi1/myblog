import click
from myblog.extensions import db

def register_commands(app):
    @app.cli.command
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

        # click.echo("生成评论")
        # fake_comments(comment)

        click.echo("生成完成")


