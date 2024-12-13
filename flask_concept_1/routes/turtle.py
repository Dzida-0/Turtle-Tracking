from flask import render_template, flash, Blueprint

turtle_bp = Blueprint('turtle', __name__)


@turtle_bp.route('/')
def index():
    return render_template('turtle.html')
