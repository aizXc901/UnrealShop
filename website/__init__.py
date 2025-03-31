from flask import Flask, render_template
from .db import db


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html')

    with app.app_context():
        from . import models
        db.create_all()

    from . import views
    app.register_blueprint(views.views)

    return app
