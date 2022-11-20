import logging

from flask import Blueprint, Flask, jsonify, redirect, url_for
from flask_restx import Api

from emannotationschemas.blueprint_app import api_bp
from emannotationschemas.config import configure_app
from emannotationschemas.utils import get_instance_folder_path
from emannotationschemas.views import views_bp

__version__ = "5.4.0"


def create_app(test_config=None):

    # Define the Flask Object
    app = Flask(
        __name__,
        instance_path=get_instance_folder_path(),
        static_url_path="/schema/static",
        instance_relative_config=True,
    )

    logging.basicConfig(level=logging.DEBUG)

    # load configuration (from test_config if passed)
    if test_config is None:
        app = configure_app(app)
    else:
        app.config.update(test_config)

    apibp = Blueprint("api", __name__, url_prefix="/schema/api")

    @app.route("/schema/versions")
    def versions():
        return jsonify([2]), 200

    @app.route("/schema/")
    def index():
        return redirect("/schema/views")

    with app.app_context():
        api = Api(
            apibp, title="EMAnnotationSchemas API", version=__version__, doc="/doc"
        )
        api.add_namespace(api_bp, path="/v2")
        app.register_blueprint(apibp)
        app.register_blueprint(views_bp)

    return app
