from flask import render_template, Blueprint, abort

from flask_concept_1.models import Turtle

turtle_bp = Blueprint('turtle', __name__)


@turtle_bp.route('/turtles')
def turtles():
    turtles = Turtle.query.all()
    if not turtles:
        abort(404)
    return render_template('turtles.html', turtles=turtles)

@turtle_bp.route('/turtle/<int:turtle_id>')
def turtle(turtle_id):
    turtle = Turtle.query.get(turtle_id)  # Fetching the turtle with the given id
    if not turtle:
        abort(404)
    return render_template('turtle.html', turtle=turtle)
