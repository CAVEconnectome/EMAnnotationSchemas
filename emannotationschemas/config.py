# Define the application directory
import os
from emannotationschemas.utils import get_app_base_path
import logging


class BaseConfig(object):
    HOME = os.path.expanduser("~")
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    # Statement for enabling the development environment
    DEBUG = True
    proj_dir = os.path.split(get_app_base_path())[0]

    LOGGING_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
    LOGGING_LOCATION = HOME + '/emannotationschema/bookshelf.log'
    LOGGING_LEVEL = logging.DEBUG

config = {
    "development": "emannotationschemas.config.BaseConfig",
    "testing": "emannotationschemas.config.BaseConfig",
    "default": "emannotationschemas.config.BaseConfig"
}


def configure_app(app):
    config_name = os.getenv('FLASK_CONFIGURATION', 'default')
    # object-based default configuration
    app.config.from_object(config[config_name])
    if 'EMANNOTATION_SCHEMA_SETTINGS' in os.environ.keys():
        app.config.from_envvar('EMANNOTATION_SCHEMA_SETTINGS')
    # instance-folders configuration
    app.config.from_pyfile('config.cfg', silent=True)

    return app
