from emannotationschemas.base import ReferenceAnnotation
import marshmallow as mm
from marshmallow.validate import OneOf

allowed_bouton_categories = ['pancake',
                            'basmati',
                            'potato',
                            'sst',
                            'vertical',
                            'vip',
                            'ivy',
                            'clutch',
                            'chandelier',
                            'unknown',
                            ]

class PresynapticBoutonType( ReferenceAnnotation ):

    target_id = mm.fields.Int(
        required=True,
        description='Synapse Annotation Id Referenced',
        reference_type='synapse')

    bouton_type = mm.fields.Str(
        required=True,
        validate=OneOf( allowed_bouton_categories ),
        description='Presynaptic type based on bouton')

    @mm.post_load
    def validate_type(self, item):
        assert item['type'] == 'presynaptic_bouton_type'