from datetime import datetime

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
)

from app import db
from . import bp
from .models import Post
from .forms import PostForm


@bp.route("", methods=["GET"])
def list_posts():
    """Display all active posts ordered by publish date descending."""
    stmt = db.select(Post).where(Post.is_active.is_(True)).order_by(Post.posted.desc())
    posts = db.session.scalars(stmt).all()
    return render_template("posts/posts.html", posts=posts)


@bp.route("/create", methods=["GET", "POST"])
def create_post():
    """Create a new post using PostForm."""
    form = PostForm()
    if form.validate_on_submit():
        posted = form.publish_date.data or datetime.utcnow()

        post = Post(
            title=form.title.data,
            content=form.content.data,
            posted=posted,
            is_active=form.enabled.data,
            category=form.category.data,
        )

        # Author is taken from session if present
        username = session.get("username")
        if username:
            post.author = username

        db.session.add(post)
        db.session.commit()
        flash("Post created successfully", "success")
        return redirect(url_for("posts.detail_post", id=post.id))

    return render_template("posts/add_post.html", form=form, title="Create post")


@bp.route("/<int:id>", methods=["GET"])
def detail_post(id: int):
    """Show full information for a single post."""
    post = db.get_or_404(Post, id)
    return render_template("posts/detail_post.html", post=post)


@bp.route("/<int:id>/update", methods=["GET", "POST"])
def update_post(id: int):
    """Edit an existing post."""
    post = db.get_or_404(Post, id)
    form = PostForm(obj=post)

    # Manual mapping for fields with different names
    if request.method == "GET" and post.posted:
        form.publish_date.data = post.posted
        form.enabled.data = post.is_active

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.posted = form.publish_date.data or post.posted
        post.is_active = form.enabled.data
        post.category = form.category.data

        db.session.commit()
        flash("Post updated successfully", "success")
        return redirect(url_for("posts.detail_post", id=post.id))

    return render_template("posts/add_post.html", form=form, title="Edit post")


@bp.route("/<int:id>/delete", methods=["GET", "POST"])
def delete_post(id: int):
    """Delete a post after confirmation."""
    post = db.get_or_404(Post, id)

    if request.method == "POST":
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted", "info")
        return redirect(url_for("posts.list_posts"))

    return render_template("posts/delete_confirm.html", post=post)
