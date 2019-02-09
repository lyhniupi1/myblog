from flask import render_template, flash, redirect, url_for, request, current_app, Blueprint
from flask_login import login_required, current_user

from myblog.extensions import db
from myblog.forms import SettingForm, PostForm, CategoryForm, LinkForm
from myblog.models import Post, Category, Comment, Link
from myblog.utils import redirect_back


admin_bp = Blueprint("admin",__name__)



@admin_bp.before_request
@login_required
def login_protect():
    pass


# post
@admin_bp.route("/post/new",methods=["GET","POST"])
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        category = Category.query.get(form.category.data)
        post = Post(title=title, body=body, category=category)
        db.session.add(post)
        db.session.commit()
        flash("post created", "success")
        return redirect(url_for("blog.show_post", post_id=post.id))
    return render_template("admin/new_post.html", form=form)


@admin_bp.route("/post/edit/<int:post_id>",methods=["GET","POST"])
def edit_post(post_id):
    post = Post.query.get(post_id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        post.category = Category.query.get(form.category.data)
        db.session.commit()
        flash("edit success!", "success")
        return redirect(url_for("blog.show_post", post_id=post.id))
    form.category.data = post.category_id
    form.title.data = post.title
    form.body.data = post.body
    return render_template("admin/edit_post.html", form=form)


@admin_bp.route("/post/delete/<int:post_id>", methods=["POST"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("blog.index"))


@admin_bp.route("/manage_post", methods=["GET", "POST"])
def manage_post():
    categories = Category.query.all()
    page = request.args.get("page", 1, type=int)
    per_page = current_app.config.get("MYBLOG_POST_PER_PAGE")
    filter_rule = request.args.get("filter", "all")  #  all category
    if filter_rule == "all":
        filtered_posts = Post.query.order_by(Post.timestamp.desc())
    else:
        filtered_posts = db.session.query(Post).join(Category).filter(Category.name == filter_rule).order_by(Post.timestamp.desc())
    pagination = filtered_posts.paginate(page, per_page=per_page)
    posts = pagination.items
    return render_template("admin/manage_post.html", pagination=pagination, posts=posts, categories=categories)


# comment
@admin_bp.route("/post/set_comment/<int:post_id>", methods=["POST"])
def set_comment(post_id):
    post = Post.query.get_or_404(post_id)
    if post.can_comment :
        post.can_comment = False
        flash("Comment disabled", "success")
    else:
        post.can_comment = True
        flash("Comment enabled", "success")
    db.session.commit()
    return redirect_back()


@admin_bp.route("/post/delete_comment/<int:comment_id>", methods=["POST"])
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    return redirect_back()


@admin_bp.route("/manage_comment", methods=["GET","POST"])
def manage_comment():
    page = request.args.get("page", 1, type=int)
    per_page = current_app.config.get("MYBLOG_COMMENT_PER_PAGE")
    filter_rule = request.args.get("filter", "all")  #  all unread admin
    if filter_rule == 'unread':
        filtered_comments = Comment.query.filter_by(reviewed=False).order_by(Comment.timestamp.desc())
    elif filter_rule == 'admin':
        filtered_comments = Comment.query.filter_by(from_admin=True).order_by(Comment.timestamp.desc())
    else:
        filtered_comments = Comment.query.order_by(Comment.timestamp.desc())

    pagination = filtered_comments.paginate(page, per_page=per_page)
    comments = pagination.items
    return render_template("admin/manage_comment.html", pagination=pagination, comments=comments)


@admin_bp.route("/approve_comment/<int:comment_id>", methods=["POST"])
def approve_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    comment.reviewed = True
    db.session.commit()
    return redirect_back()


# category
@admin_bp.route("/new_category", methods=["GET","POST"])
def new_category():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data)
        db.session.add(category)
        db.session.commit()
        return redirect(url_for("blog.index"))
    return render_template("/admin/new_category.html", form=form)


@admin_bp.route("/manage_category")
def manage_category():
    categories = Category.query.all()
    return render_template("admin/manage_category.html", categories=categories)


@admin_bp.route("/edit_category/<int:category_id>", methods=["GET","POST"])
def edit_category(category_id):
    category = Category.query.get_or_404(category_id)
    form = CategoryForm()
    if category.id == 1:
        flash('You can not edit the default category.', 'warning')
        return redirect_back()
    if form.validate_on_submit():
        category.name = form.name.data
        db.session.commit()
        flash('Category updated.', 'success')
        return redirect(url_for('.manage_category'))

    form.name.data = category.name
    return render_template("admin/edit_category.html", form=form)


@admin_bp.route("/delete_category/<int:category_id>", methods=["POST"])
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    if category.id == 1:
        flash('You can not delete the default category.', 'warning')
        return redirect_back()
    category.delete()
    return redirect_back()


# link
@admin_bp.route("/new_link", methods=["GET","POST"])
def new_link():
    form = LinkForm()
    if form.validate_on_submit():
        link = Link(name=form.name.data, url=form.url.data)
        db.session.add(link)
        db.session.commit()
        return redirect(url_for("blog.index"))
    return render_template("/admin/new_link.html", form=form)


@admin_bp.route("/manage_link", methods=["GET","POST"])
def manage_link():
    links = Link.query.all()
    return render_template("admin/manage_link.html", links=links)


@admin_bp.route("/edit_link/<int:link_id>", methods=["GET","POST"])
def edit_link(link_id):
    link = Link.query.get_or_404(link_id)
    form = LinkForm()
    if form.validate_on_submit():
        link.url = form.url.data
        link.name = form.name.data
        db.session.commit()
        return redirect_back()
    form.name.data = link.name
    form.url.data = link.url
    return render_template("admin/edit_link.html", form=form)

@admin_bp.route("/delete_link/<int:link_id>", methods=["POST"])
def delete_link(link_id):
    link = Link.query.get_or_404(link_id)
    db.session.delete(link)
    db.session.commit()
    return redirect(url_for("admin.manage_link"))


#settings
@admin_bp.route("/settings", methods=["GET","POST"])
def settings():
    form = SettingForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.blog_title = form.blog_title.data
        current_user.blog_sub_title = form.blog_sub_title.data
        current_user.about = form.about.data
        db.session.commit()
        flash('Setting updated.', 'success')
        return redirect(url_for('blog.index'))
    form.name.data = current_user.name
    form.blog_title.data = current_user.blog_title
    form.blog_sub_title.data = current_user.blog_sub_title
    form.about.data = current_user.about
    return render_template('admin/settings.html', form=form)


