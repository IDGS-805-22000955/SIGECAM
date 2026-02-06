from flask import Flask
from config import config
from app.extensions import bcrypt, close_db


def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    bcrypt.init_app(app)
    app.teardown_appcontext(close_db)

    #  DASHBOARD DE ADMIN
    from app.admin.routes import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # LOGIN
    from app.auth.routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/')

    # DASHBOAR DE USUARIO
    from app.user.routes import user_bp
    app.register_blueprint(user_bp, url_prefix='/user')

    return app