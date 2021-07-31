import os


class BaseConfig:
    APPS = [
        'src.apps.blog',
        'src.apps.user',
    ]
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    PASSWORD_PATTERN = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})'


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    DATABASE = {
        'URI': f'sqlite:///{BaseConfig.BASE_DIR}/sqlite.db'
    }


class ProductionConfig(BaseConfig):
    DEBUG = False


def get_config():
    env = os.environ.get('FLASK_ENV')

    if env == 'development':
        return DevelopmentConfig
    elif env == 'production':
        return ProductionConfig

    raise EnvironmentError('FLASK_ENV is not set')
