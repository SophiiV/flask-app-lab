from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    request,
)

from sqlalchemy import select

from app import db
from . import bp
from .models import Post, Tag
from .forms import PostForm


@bp.route("/", methods=["GET"])
def list_posts():
    stmt = select(Post).order_by(Post.posted.desc())
    posts = db.session.scalars(stmt).all()
    return render_template("posts/posts.html", posts=posts)


@bp.route("/create", methods=["GET", "POST"])
def create_post():
    form = PostForm()

    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            category=form.category.data,
            author_id=form.author_id.data or None,
        )

        post.tags = []
        for tag_id in form.tags.data:
            tag = db.session.get(Tag, tag_id)
            if tag:
                post.tags.append(tag)

        db.session.add(post)
        db.session.commit()
        flash("Post created successfully", "success")
        return redirect(url_for("posts.list_posts"))

    return render_template("posts/add_post.html", form=form)


@bp.route("/<int:post_id>", methods=["GET"])
def detail_post(post_id: int):
    post = db.get_or_404(Post, post_id)
    return render_template("posts/detail_post.html", post=post)


@bp.route("/<int:post_id>/update", methods=["GET", "POST"])
def update_post(post_id: int):
    post = db.get_or_404(Post, post_id)
    form = PostForm(obj=post)

    if request.method == "GET":
        form.author_id.data = post.author_id
        form.tags.data = [tag.id for tag in post.tags]

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.category = form.category.data
        post.author_id = form.author_id.data or None

        # оновлюємо список тегів
        post.tags.clear()
        for tag_id in form.tags.data:
            tag = db.session.get(Tag, tag_id)
            if tag:
                post.tags.append(tag)

        db.session.commit()
        flash("Post updated successfully", "success")
        return redirect(url_for("posts.detail_post", post_id=post.id))

    return render_template("posts/add_post.html", form=form, post=post)


@bp.route("/<int:post_id>/delete", methods=["GET", "POST"])
def delete_post(post_id: int):
    post = db.get_or_404(Post, post_id)

    if request.method == "POST":
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted", "info")
        return redirect(url_for("posts.list_posts"))

    return render_template("posts/delete_confirm.html", post=post)
