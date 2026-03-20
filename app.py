from flask import Flask
from config import config
from project.extensions import bcrypt, db, migrate

from project.admin.routes import admin_bp
from project.auth.routes import auth_bp
from project.user.routes import user_bp
from project.modules.pedidos.routes import pedidos_bp
import models

app = Flask(__name__, template_folder='project/templates', static_folder='project/static', static_url_path='/static')
app.config.from_object(config['development'])


db.init_app(app)
migrate.init_app(app, db)
bcrypt.init_app(app)

app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(auth_bp, url_prefix='/')
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(pedidos_bp, url_prefix='/pedidos')


@app.errorhandler(404)
def page_not_found(e):
    return "Página no encontrada", 404


if __name__ == '__main__':
    app.run(port=5000, debug=True)