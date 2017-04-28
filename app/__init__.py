from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config

try:
    from wtforms.fields import HiddenField
except ImportError:

    def is_hidden_field_filter(field):
        raise RuntimeError('WTForms is not installed.')
else:

    def is_hidden_field_filter(field):
        return isinstance(field, HiddenField)



mail = Mail()
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    app.jinja_env.globals['is_hidden_field'] = is_hidden_field_filter

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .quote import quote as quote_blueprint
    app.register_blueprint(quote_blueprint, url_prefix='/quote')

    from .tools import tools as tools_blueprint
    app.register_blueprint(tools_blueprint, url_prefix='/tools')

    from .irclog import irclog as irclog_blueprint
    app.register_blueprint(irclog_blueprint, url_prefix='/irclog')

    return app
