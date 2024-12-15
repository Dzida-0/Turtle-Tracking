import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'

    # Ensure 'instance' folder exists
    instance_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance')
    if not os.path.exists(instance_path):
        os.makedirs(instance_path)

    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(instance_path, "database.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
