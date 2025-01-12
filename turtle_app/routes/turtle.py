import logging
import os

import boto3
from flask import render_template, Blueprint, abort, request, jsonify, session, send_from_directory, url_for, \
    current_app
from flask_login import current_user, user_logged_out, user_logged_in

from .main import create_interactive_map
from ..extensions import db
from turtle_app.models import Turtle, TurtlePosition

turtle_bp = Blueprint('turtle', __name__)


@turtle_bp.route('/turtles')
def turtles():
    all_turtles = Turtle.query.all()
    if not all_turtles:
        abort(500)
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
    if not positions:
        return "No positions available for this turtle.", 404
    map_path = create_interactive_map(positions)
    return send_from_directory(map_path,'generated_map.html')


@turtle_bp.route('/photos/<filename>')
def serve_photo(filename):
    base_dir = current_app.root_path
    photos_dir = os.path.join(base_dir, 'storage', 'photos')
    photos_dir = photos_dir.replace('turtle_app' + os.sep, '')
    return send_from_directory(photos_dir, filename)


@turtle_bp.route('/turtle/<int:turtle_id>')
def turtle(turtle_id):
    turtle = Turtle.query.get(turtle_id)
    positions = TurtlePosition.query.get(turtle_id)
    # Fetching the turtle with the given id
    if not turtle:
        abort(404)

    flask_config = os.getenv('FLASK_CONFIG', 'development')

    # Default picture
    picture_url = None

    if flask_config == 'development':
        # Check local storage for turtle_{turtle_id}.png
        picture_url = url_for('turtle.serve_photo', filename=f'turtle_{turtle_id}.png')

    elif flask_config == 'production':
        # Check S3 bucket for turtle_{turtle_id}.png
        s3_bucket = os.getenv('S3_BUCKET_NAME')
        s3_client = boto3.client('s3')

        # Check if the file exists in the S3 bucket
        try:
            s3_client.head_object(Bucket=s3_bucket, Key=f'photos/turtle_{turtle_id}.png')
            picture_url = f'https://{s3_bucket}.s3.amazonaws.com/photos/turtle_{turtle_id}.png'
        except s3_client.exceptions.ClientError:
            # File does not exist, use default picture
            pass

    # Fall back to a default picture
    if not picture_url:
        picture_url = url_for('static', filename='pictures/turtle.png')

    all_turtles = Turtle.query.all()
    if not all_turtles:
        abort(500)
    favorites = []

    if current_user.is_authenticated:
        favorites = current_user.favorites
    else:
        session_favorites = session.get('favorites', [])
        favorites = Turtle.query.filter(Turtle.id.in_(session_favorites)).all()

    return render_template('turtle.html', turtle=turtle, positions=positions, picture_url=picture_url,favorites=favorites)


@turtle_bp.route('/update_favorite', methods=['POST'])
def update_favorite():
    data = request.get_json()
    logging.warning(data)
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
