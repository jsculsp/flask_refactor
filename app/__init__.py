from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_moment import Moment
from flask_pagedown import PageDown

from config import config
from .mail.email import mail
from .models import db

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

bootstrap = Bootstrap()
moment = Moment()
pagedown = PageDown()


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)

    from .routes import global_main as routes_global
    app.register_blueprint(routes_global)

    from .routes.main.main import main as routes_user
    app.register_blueprint(routes_user)

    from .routes.auth.auth import main as routes_auth
    app.register_blueprint(routes_auth, url_prefix='/auth')

    return app
