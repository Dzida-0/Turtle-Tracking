from flask_concept_1.extensions import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    is_active = db.Column(db.Boolean, default=True)


class Turtle(db.Model):
    __tablename__ = 'turtle'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    last_position = db.Column(db.String(100))
    is_active = db.Column(db.Boolean)
    turtle_sex = db.Column(db.String(10))
    turtle_age = db.Column(db.String(20))
    length = db.Column(db.Float)
    length_type = db.Column(db.String(20))
    width = db.Column(db.Float)
    width_type = db.Column(db.String(20))
    project_name = db.Column(db.String(100))
    biography = db.Column(db.Text)
    description = db.Column(db.Text)



class TurtlePosition(db.Model):
    __tablename__ = 'turtle_pos'
    id = db.Column(db.Integer, primary_key=True)
    turtle_id = db.Column(db.Integer, nullable = False)
