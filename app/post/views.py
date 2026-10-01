from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.extensions import db
from app.post.models import Post, Category
from app.user.decorators import login_required

blueprint = Blueprint("post", __name__, url_prefix="/post")


@blueprint.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == 'GET':
        categories = Category.query.all()
        return render_template("post/create.html", categories=categories)

    # bagian POST: simpan postingan baru
    title = request.form.get("title")
    body = request.form.get("body")
    category_ids = request.form.getlist("categories")

    post = Post(
        title=title,
        body=body,
        user_id=session["user_id"],
    )

    if category_ids:
        post.categories = Category.query.filter(Category.id.in_(category_ids)).all()

    db.session.add(post)
    db.session.commit()

    flash("Post berhasil dibuat.", "success")
    return redirect(url_for("public.home"))


@blueprint.route('/delete/<int:post_id>', methods=["POST"])
@login_required
def delete(post_id):
    post = Post.query.get_or_404(post_id)

    # hanya pemilik postingan yang boleh menghapus
    if post.user_id != session["user_id"]:
        flash("Kamu tidak boleh menghapus postingan orang lain.", "error")
        return redirect(url_for("public.home"))

    db.session.delete(post)
    db.session.commit()

    flash("Post berhasil dihapus.", "success")
    return redirect(url_for("public.home"))

@blueprint.route('/<int:post_id>')
@login_required
def detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post/detail.html', post=post)

@blueprint.route('/category/<int:category_id>')
@login_required
def category(category_id):
    category = Category.query.get_or_404(category_id)
    posts = (
        Post.query
        .filter(Post.categories.contains(category))
        .order_by(Post.id.desc())
        .all()
    )
    return render_template('post/category.html', category=category, posts=posts)