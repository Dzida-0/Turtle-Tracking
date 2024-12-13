from flask import Flask

from .extensions import db,login_manager,csrf
from .routes.main import main_bp
from .routes.turtle import turtle_bp
from .routes.auth import auth_bp


app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)
login_manager.init_app(app)
csrf.init_app(app)
# Blueprints
app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(turtle_bp)

from .errors import page_not_found,internal_server_error