from flask import render_template, Blueprint, abort, request, jsonify, session
from flask_login import current_user, user_logged_out, user_logged_in

from .main import create_interactive_map
from ..extensions import db
from flask_concept_1.models import Turtle, TurtlePosition

turtle_bp = Blueprint('turtle', __name__)


@turtle_bp.route('/turtles')
def turtles():
    all_turtles = Turtle.query.all()
    if not all_turtles:
        abort(404)
    favorites = []

    if current_user.is_authenticated:
        favorites = current_user.favorites
    else:
        session_favorites = session.get('favorites', [])
        favorites = Turtle.query.filter(Turtle.id.in_(session_favorites)).all()

    return render_template('turtles.html', turtles=all_turtles, favorites=favorites)


@turtle_bp.route('/generated_map<int:turtle_id>')
def generated_map(turtle_id):
    positions = TurtlePosition.query.filter_by(turtle_id=turtle_id).all()
    map_path = create_interactive_map(positions)
    if not positions:
        return "No positions available for this turtle.", 404
    return render_template('maps/generated_map.html')


@turtle_bp.route('/turtle/<int:turtle_id>')
def turtle(turtle_id):
    turtle = Turtle.query.get(turtle_id)
    positions = TurtlePosition.query.get(turtle_id)
    # Fetching the turtle with the given id
    if not turtle:
        abort(404)
    return render_template('turtle.html', turtle=turtle, positions =positions)


@turtle_bp.route('/update_favorite', methods=['POST'])
def update_favorite():
    data = request.get_json()
    turtle_id = data.get('turtle_id')
    is_favorite = data.get('favorite')

    if not turtle_id:
        return jsonify({'success': False, 'error': 'Turtle ID is missing'}), 400

    if current_user.is_authenticated:
        # Update the database for the logged-in user
        turtle = Turtle.query.get(turtle_id)
        if not turtle:
            return jsonify({'success': False, 'error': 'Turtle not found'}), 404

        if is_favorite:
            if turtle not in current_user.favorites:
                current_user.favorites.append(turtle)
        else:
            if turtle in current_user.favorites:
                current_user.favorites.remove(turtle)

        db.session.commit()
    else:
        # Update the session for guests
        session_favorites = session.get('favorites', [])
        if is_favorite:
            if turtle_id not in session_favorites:
                session_favorites.append(turtle_id)
        else:
            if turtle_id in session_favorites:
                session_favorites.remove(turtle_id)
        session['favorites'] = session_favorites

    return jsonify({'success': True})


@user_logged_out.connect_via(turtle_bp)
def clear_session_favorites(sender, user):
    session.pop('favorites', None)


@user_logged_in.connect_via(turtle_bp)
def merge_favorites(sender, user):
    session_favorites = session.get('favorites', [])
    if session_favorites:
        turtles = Turtle.query.filter(Turtle.id.in_(session_favorites)).all()
        user.favorites.extend(turtle for turtle in turtles if turtle not in user.favorites)
        db.session.commit()
        session.pop('favorites', None)
