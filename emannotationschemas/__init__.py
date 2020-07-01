from emannotationschemas.schemas.synapse import SynapseSchema, PlasticSynapse
from emannotationschemas.schemas.presynaptic_bouton_type import PresynapticBoutonType
from emannotationschemas.schemas.functional_coregistration import FunctionalCoregistration
from emannotationschemas.schemas.postsynaptic_compartment import PostsynapticCompartment
from emannotationschemas.schemas.base import FlatSegmentationReferenceSinglePoint
from emannotationschemas.schemas.cell_type_local import CellTypeLocal
from emannotationschemas.schemas.bound_text_tag import BoundTagAnnotation
from emannotationschemas.schemas.glia_contact import GliaContact
from emannotationschemas.schemas.contact import Contact
from emannotationschemas.schemas.extended_classical_cell_type import ExtendedClassicalCellType

from emannotationschemas.errors import UnknownAnnotationTypeException
from emannotationschemas.flatten import create_flattened_schema

__version__ = '2.1.0'

type_mapping = {
    'synapse': SynapseSchema,
    'presynaptic_bouton_type': PresynapticBoutonType,
    'postsynaptic_compartment': PostsynapticCompartment,
    'microns_func_coreg': FunctionalCoregistration,
    'cell_type_local': CellTypeLocal,
    'nucleus_detection': FlatSegmentationReferenceSinglePoint,
    'bound_tag': BoundTagAnnotation,
    'extended_classical_cell_type': ExtendedClassicalCellType,
    'plastic_synapse': PlasticSynapse,
    'glia_contact': GliaContact,
    'contact': Contact,
}


def get_types():
    return [k for k in type_mapping.keys()]


def get_schema(type):
    try:
        return type_mapping[type]
    except KeyError:
        msg = 'type {} is not a known annotation type'.format(type)
        raise UnknownAnnotationTypeException(msg)


def get_flat_schema(type):
    try:
        Schema = type_mapping[type]
        FlatSchema = create_flattened_schema(Schema)
        return FlatSchema
    except KeyError:
        msg = 'type {} is not a known annotation type'.format(type)
        raise UnknownAnnotationTypeException(msg)


def create_app(test_config=None):
    from flask import Flask, jsonify, url_for, redirect, Blueprint
    from flask_restx import Api

    from emannotationschemas.config import configure_app
    from emannotationschemas.utils import get_instance_folder_path

    from emannotationschemas.blueprint_app import api_bp 
    from emannotationschemas.views import views_bp
    import logging
    # Define the Flask Object
    app = Flask(__name__,
                instance_path=get_instance_folder_path(),
                instance_relative_config=True)

    logging.basicConfig(level=logging.DEBUG)

    # load configuration (from test_config if passed)
    if test_config is None:
        app = configure_app(app)
    else:
        app.config.update(test_config)

    apibp = Blueprint('api', __name__, url_prefix='/schema/api')
    with app.app_context():
        api = Api(apibp, title="EMAnnotationSchemas API", version=__version__, doc="/doc")
        api.add_namespace(api_bp, path='/v2')
        app.register_blueprint(apibp)
        app.register_blueprint(views_bp)

    return app