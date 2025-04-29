from flask import Flask, render_template
from flask_login import LoginManager, current_user
from .db import db, migrate
from .models import User


def create_app():
    app = Flask(__name__, static_folder='../static')
    app.secret_key = 'secretKey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)  # Если используете Flask-Migrate

    # Регистрация Blueprints и т.д.
    from .views import views
    from .auth import auth
    app.register_blueprint(views)
    app.register_blueprint(auth)

    with app.app_context():
        db.create_all()  # Создаёт таблицы при запуске приложения

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app