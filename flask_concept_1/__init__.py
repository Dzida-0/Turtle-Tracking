import os

from flask import Flask

from .extensions import db, login_manager, csrf
from .models import Turtle
from .routes.main import main_bp
from .routes.turtle import turtle_bp
from .routes.auth import auth_bp
from data.download_data import download_turtles_info,download_turtles_positions
from data.data_parsing import parse_turtle_info,parse_turtle_positions

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)
login_manager.init_app(app)
csrf.init_app(app)
#


# Blueprints
app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(turtle_bp)

from .errors import page_not_found, internal_server_error

with app.app_context():
    db.create_all()
    #download_turtles_info()
    #parse_turtle_info()
    #turtles = Turtle.query.all()
    #for turtle in turtles:
        #parse_turtle_positions(turtle.id)
        #download_turtles_positions(turtle.id)

