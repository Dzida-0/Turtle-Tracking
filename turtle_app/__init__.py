import logging
import os
from flask import Flask
from config import config
from .extensions import db, login_manager, csrf
from .models import Turtle
from .routes.main import main_bp
from .routes.turtle import turtle_bp
from .routes.auth import auth_bp
from data.download_data import download_turtles_info, download_turtles_positions
from data.data_parsing import parse_turtle_info, parse_turtle_positions
from .errors import create_error_handlers
from flask_assets import Environment, Bundle

def create_app():
    application = Flask(__name__)
    application.config.from_object(config[os.getenv('FLASK_CONFIG', 'development')])
    db.init_app(application)
    login_manager.init_app(application)
    assets = Environment(application)
    scss = Bundle('static/styles.scss', filters='scss', output='static/styles.css')
    assets.register('scss_all', scss)

    csrf.init_app(application)

    # Blueprints
    application.register_blueprint(main_bp)
    application.register_blueprint(auth_bp)
    application.register_blueprint(turtle_bp)

    create_error_handlers(application)
    with application.app_context():
        db.create_all()
        # download_turtles_info()
        # parse_turtle_info()
        # turtles = Turtle.query.all()
        # for turtle in turtles:
        # parse_turtle_positions(turtle.id)
        # download_turtles_positions(turtle.id)
    return application
