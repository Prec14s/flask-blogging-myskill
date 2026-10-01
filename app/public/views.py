from flask import Blueprint, render_template
from app.post.models import Post
from app.user.decorators import login_required

blueprint = Blueprint( "public", __name__, url_prefix="/")

@blueprint.route('/')
@login_required
def home():
    posts = Post.query.order_by(Post.id.desc()).all()
    return render_template('home.html', posts=posts)


   

