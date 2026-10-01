from flask import Flask, render_template, request
from app.config import Config
from app.extensions import db, migrate, login_manager
from app import public, user, post
from app.user.models import User
from app.extensions import db
from app.post.models import Category


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    register_login_manager(app)


def register_login_manager(app):
    login_manager.init_app(app)


    @login_manager.user_loader
    def load_user (user_id):
        return User.query.get(user_id)


def register_blueprints(app):
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(user.views.blueprint)
    app.register_blueprint(post.views.blueprint)



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    register_extensions(app)
    register_blueprints(app)
    
    @app.errorhandler(401)
    def unauthorized(error):
        return render_template('401.html'), 401

    @app.context_processor
    def inject_categories():
        return {"sidebar_categories": Category.query.order_by(Category.name).all()}

    return app