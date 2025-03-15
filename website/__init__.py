from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()
DB_NAME = 'database.sqlite3'


def create_database():
    db.create_all()
    print('Database Created')

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    db.init_app(app)

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html')

    from .views import views

    app.register_blueprint(views, url_prefix='/')

    with app.app_context():
         create_database()

    return app