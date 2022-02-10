from flask import Flask
from flask_login import LoginManager
from .main.routes import auth
from .extenstions import db
from flask_bootstrap import Bootstrap


def create_app():
    app = Flask(__name__)
    bootstrap = Bootstrap(app)
    app.config['SECRET_KEY'] = '2313'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
     

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User
     
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    from .main.routes import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app