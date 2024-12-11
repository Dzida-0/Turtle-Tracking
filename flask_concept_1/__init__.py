from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_concept_1 import errors

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)