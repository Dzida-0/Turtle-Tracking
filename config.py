import logging
import os


# basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret string')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    logging.info("4")
    instance_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance')
    if not os.path.exists(instance_path):
        os.makedirs(instance_path)
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(instance_path, "database.db")}'


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'  # in-memory database


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    IMAGE_FOLDER = os.path.join(os.getcwd(), 'static', 'images')
    AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')

    # Update with RDS PostgreSQL credentials
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'postgresql://username:password@your-rds-endpoint:5432/your-database-name'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
