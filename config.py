import os


class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret string')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    instance_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance')
    if not os.path.exists(instance_path):
        os.makedirs(instance_path)
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(instance_path, "database.db")}'
    storage_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'storage')
    if not os.path.exists(storage_path):
        os.makedirs(storage_path)
    STORAGE_PATH = storage_path
    for catalog in ['maps','photos','json']:
        if not os.path.exists(f"{storage_path}/{catalog}"):
            os.makedirs(f"{storage_path}/{catalog}")


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
