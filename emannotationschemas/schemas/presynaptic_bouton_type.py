from emannotationschemas.schemas.base import ReferenceAnnotation
import marshmallow as mm
from marshmallow.validate import OneOf
from marshmallow import validates_schema, ValidationError

allowed_bouton_categories = ['pancake',
                            'basmati',
                            'potato',
                            'sst',
                            'vertical',
                            'vip',
                            'ivy',
                            'clutch',
                            'chandelier',
                            ]

class PresynapticBoutonType(ReferenceAnnotation):

    target_id = mm.fields.Int(
        required=True,
        description='Synapse annotation id reference',
        reference_type='synapse')

    bouton_type = mm.fields.Str(
        required=True,
        validate=OneOf(allowed_bouton_categories),
        description='Presynaptic type based on bouton')

