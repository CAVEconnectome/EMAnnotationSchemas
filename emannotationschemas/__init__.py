from emannotationschemas.synapse import SynapseSchema
from emannotationschemas.errors import UnknownAnnotationTypeException
from emannotationschemas.flatten import create_flattened_schema
from emannotationschemas.presynaptic_bouton_type import PresynapticBoutonType
from emannotationschemas.functional_coregistration import FunctionalCoregistration
from emannotationschemas.postsynaptic_compartment import PostsynapticCompartment
from emannotationschemas.base import FlatSegmentationReference
from emannotationschemas.cell_type_local import CellTypeLocal
from emannotationschemas.bound_text_tag import BoundTagAnnotation
from emannotationschemas.extended_classical_cell_type import ExtendedClassicalCellType

__version__ = '1.1.1'

type_mapping = {
    'synapse': SynapseSchema,
    'presynaptic_bouton_type': PresynapticBoutonType,
    'postsynaptic_compartment': PostsynapticCompartment,
    'microns_func_coreg': FunctionalCoregistration,
    'cell_type_local': CellTypeLocal,
    'flat_segmentation_reference': FlatSegmentationReference,
    'bound_tag': BoundTagAnnotation,
    'extended_classical_cell_type': ExtendedClassicalCellType,
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