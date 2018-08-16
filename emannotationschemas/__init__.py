from emannotationschemas.synapse import SynapseSchema
from emannotationschemas.tags import BoundTagAnnotation,\
                                     TypedReferenceTags
from emannotationschemas.errors import UnknownAnnotationTypeException
from emannotationschemas.flatten import create_flattened_schema
from emannotationschemas.bouton_shape import BoutonShape
from emannotationschemas.functional_coregistration import FunctionalCoregistration
__version__ = '0.2.0'

type_mapping = {
    'synapse': SynapseSchema,
    'bouton_shape': BoutonShape,
    'functional_coregistration': FunctionalCoregistration,
    'bound_tag': BoundTagAnnotation,
}
for ref_type in TypedReferenceTags:
    type_mapping['{}_reference_tag'.format(ref_type)] = TypedReferenceTags[ref_type]

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
