from flask import Flask, render_template
from flask_login import LoginManager, current_user
from .db import db

def create_app():
    app = Flask(__name__, static_folder='../static')
    app.secret_key = 'secretKey'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from .models import User
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.context_processor
    def inject_user():
        return dict(current_user=current_user)

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html')

    with app.app_context():
        from . import models
        db.create_all()

    from . import views
    from . import auth

    app.register_blueprint(views.views)
    app.register_blueprint(auth.auth)

    return app

