from flask import Flask
from flask_login import LoginManager

from website import create_app, db
from website.models import User

app1 = create_app()
def create_app():
    app = Flask(__name__)
    app.secret_key = 'secretKey'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # куда отправлять если не авторизован
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
if __name__ == '__main__':
    app1.run(debug=True)
