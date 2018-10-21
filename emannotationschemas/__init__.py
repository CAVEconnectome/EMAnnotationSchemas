from emannotationschemas.synapse import SynapseSchema
from emannotationschemas.errors import UnknownAnnotationTypeException
from emannotationschemas.flatten import create_flattened_schema
from emannotationschemas.presynaptic_bouton_type import PresynapticBoutonType
from emannotationschemas.functional_coregistration import FunctionalCoregistration
from emannotationschemas.postsynaptic_compartment import PostsynapticCompartment
from emannotationschemas.cell_type_local import CellTypeLocal

__version__ = '0.3.1'

type_mapping = {
    'synapse': SynapseSchema,
    'presynaptic_bouton_type': PresynapticBoutonType,
    'postsynaptic_compartment': PostsynapticCompartment,
    'cell_type_ai_manual': CellTypeLocal,
    'synapse_ai_manual': SynapseSchema,
    'microns_func_coreg': FunctionalCoregistration,
    'cell_type_local': CellTypeLocal,
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
    from flask import Flask
    from emannotationschemas.config import configure_app
    from emannotationschemas.utils import get_instance_folder_path

    from emannotationschemas.blueprint_app import bp 

    # Define the Flask Object
    app = Flask(__name__,
                instance_path=get_instance_folder_path(),
                instance_relative_config=True)
    # load configuration (from test_config if passed)
    if test_config is None:
        app = configure_app(app)
    else:
        app.config.update(test_config)
    # register blueprints
    app.register_blueprint(bp)

    return app