from emannotationschemas.schemas.synapse import SynapseSchema
from emannotationschemas.schemas.synapse import PlasticSynapse
from emannotationschemas.schemas.synapse import BuhmannSynapseSchema
from emannotationschemas.schemas.synapse import BuhmannEcksteinSynapseSchema
from emannotationschemas.schemas.presynaptic_bouton_type import PresynapticBoutonType
from emannotationschemas.schemas.functional_coregistration import FunctionalCoregistration, FunctionalUnitCoregistration
from emannotationschemas.schemas.postsynaptic_compartment import PostsynapticCompartment
from emannotationschemas.schemas.base import FlatSegmentationReferenceSinglePoint
from emannotationschemas.schemas.cell_type_local import CellTypeLocal
from emannotationschemas.schemas.bound_text_tag import BoundTagAnnotation
from emannotationschemas.schemas.glia_contact import GliaContact
from emannotationschemas.schemas.contact import Contact
from emannotationschemas.schemas.extended_classical_cell_type import ExtendedClassicalCellType
from emannotationschemas.schemas.nucleus_detection import NucleusDetection
from emannotationschemas.schemas.derived_spatial_point import DerivedSpatialPoint, DerivedTag
from emannotationschemas.errors import UnknownAnnotationTypeException
from emannotationschemas.flatten import create_flattened_schema

__version__ = '3.1.1'

type_mapping = {
    'synapse': SynapseSchema,
    'fly_synapse': BuhmannSynapseSchema,
    'fly_nt_synapse': BuhmannEcksteinSynapseSchema,
    'presynaptic_bouton_type': PresynapticBoutonType,
    'postsynaptic_compartment': PostsynapticCompartment,
    'microns_func_coreg': FunctionalCoregistration,
    'microns_func_unit_coreg': FunctionalUnitCoregistration,
    'cell_type_local': CellTypeLocal,
    'nucleus_detection': NucleusDetection,
    'bound_tag': BoundTagAnnotation,
    'extended_classical_cell_type': ExtendedClassicalCellType,
    'plastic_synapse': PlasticSynapse,
    'glia_contact': GliaContact,
    'contact': Contact,
    'derived_spatial_point': DerivedSpatialPoint,
    'derived_tag': DerivedTag,
}


def get_types():
    return [k for k in type_mapping.keys()]


def get_schema(schema_type: str):
    """Get schema class object by keyword, only
    returns an object that is listed in :data:`type_mapping` dict

    Parameters
    ----------
    schema_type : str
        Key name of schema in :data:`type_mapping`

    Returns
    -------
    obj
        marshmallow schema object

    Raises
    ------
    UnknownAnnotationTypeException
        Key argument is not in :data:`type_mapping` dict
    """
    try:
        return type_mapping[schema_type]
    except KeyError:
        msg = f"Schema type: {schema_type} is not a known annotation type"
        raise UnknownAnnotationTypeException(msg)


def get_flat_schema(schema_type: str):
    try:
        Schema = type_mapping[schema_type]
        FlatSchema = create_flattened_schema(Schema)
        return FlatSchema
    except KeyError:
        msg = f"Schema type: {schema_type} is not a known annotation type"
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
                static_url_path='/schema/static',
                instance_relative_config=True)

    logging.basicConfig(level=logging.DEBUG)

    # load configuration (from test_config if passed)
    if test_config is None:
        app = configure_app(app)
    else:
        app.config.update(test_config)

    apibp = Blueprint('api', __name__, url_prefix='/schema/api')
   
    @app.route('/schema/versions')
    def versions():
        return jsonify([2]), 200

    @app.route("/schema/")
    def index():
        return redirect("/schema/views")

    with app.app_context():
        api = Api(apibp, title="EMAnnotationSchemas API",
                  version=__version__, doc="/doc")
        api.add_namespace(api_bp, path='/v2')
        app.register_blueprint(apibp)
        app.register_blueprint(views_bp)

    return app
