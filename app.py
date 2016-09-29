from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment

from config import config
from mail.email import mail
from models import db

from models.role import Role
from models.user import User

bootstrap = Bootstrap()
moment = Moment()


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    from routes.user import main as routes_user
    app.register_blueprint(routes_user)

    return app

