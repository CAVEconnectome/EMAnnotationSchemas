from emannotationschemas.synapse import SynapseSchema
from emannotationschemas.errors import UnknownAnnotationTypeException
from emannotationschemas.flatten import create_flattened_schema
from emannotationschemas.bouton_shape import BoutonShape

__version__ = '0.2.0'

type_mapping = {
    'synapse': SynapseSchema,
    'bouton_shape': BoutonShape
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
