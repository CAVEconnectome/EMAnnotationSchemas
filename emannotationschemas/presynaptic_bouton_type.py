from emannotationschemas.base import ReferenceAnnotation
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

    @mm.validates_schema
    def validate_type(self, data, **kwargs):
        # check that the annotation type is present in the object as 'presynaptic_bouton_type'
        if data["type"] != 'presynaptic_bouton_type':
            raise mm.ValidationError("Type must be 'presynaptic_bouton_type'")