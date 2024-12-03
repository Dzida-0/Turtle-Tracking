from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/turtle/<int:turtle_id>")
def turtle_page(turtle_id:int):
    return f'Turte {turtle_id}'

@app.route('/login')
def login():
    return 'login'

@app.route('/register')
def login():
    return 'register'